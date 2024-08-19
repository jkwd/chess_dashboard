from dagster import AssetKey, AssetSpec, asset
from dagster_duckdb import DuckDBResource
from . import constants

import asyncio
import os
import pandas as pd
from io import StringIO
import chess
import chess.pgn
import chess.engine

username: str = os.getenv("USERNAME")

dlt_chess_players_games = AssetSpec(AssetKey("dlt_chess_players_games"))

@asset(deps=[dlt_chess_players_games], group_name="prep")
def player_games(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.execute(f"""
            SET TimeZone = 'UTC';
            CREATE SCHEMA IF NOT EXISTS chess_data_prep;
            CREATE OR REPLACE TABLE chess_data_prep.player_games as (
                with player_games as (
                    select
                    end_time
                    , url 
                    , pgn
                    , time_control
                    , rated
                    , tcn
                    , uuid
                    , initial_setup
                    , fen
                    , time_class
                    , rules
                    , white__rating
                    , white__result
                    , white__aid
                    , white__username
                    , white__uuid
                    , black__rating
                    , black__result
                    , black__aid
                    , black__username
                    , black__uuid
                    , accuracies__white
                    , accuracies__black
                    from chess_data_raw.players_games
                )
                , final as (
                    select
                    -- PLAYER DETAILS
                    if(lower(white__username)='{username}', 'White', 'Black') as player_color
                    , if(player_color = 'White', white__rating, black__rating) as player_rating
                    , if(player_color = 'White', white__result, black__result) as player_result

                    -- OPPONENT DETAILS
                    , if(player_color = 'White', black__rating, white__rating) as opponent_rating
                    , if(player_color = 'White', black__result, white__result) as opponent_result

                    -- PLAYER-OPPONENT DETAILS
                    , opponent_rating > player_rating as is_stronger_opponent
                    , case player_result
                        -- WIN
                        when 'win' then 'win'
                        
                        -- DRAW
                        when 'stalemate' then 'draw'
                        when 'agreed' then 'draw'
                        when 'repetition' then 'draw'
                        when '50move' then 'draw'
                        when 'insufficient' then 'draw'
                        when 'timevsinsufficient' then 'draw'
                        
                        -- LOSE
                        when 'checkmated' then 'lose'
                        when 'timeout' then 'lose'
                        when 'resigned' then 'lose'
                        when 'abandoned' then 'lose'
                        when 'threecheck' then 'lose'
                    end as player_wdl
                    , if(player_result='win', opponent_result, player_result) as player_wdl_reason

                    -- GAME DETAILS
                    , regexp_extract(pgn, '(ECO )"(.*)"', 2) as eco
                    , cast(replace(regexp_extract(pgn, '(UTCDate )"(.*)"', 2), '.', '-') as date) as game_start_date
                    , regexp_extract(pgn, '(StartTime )"(.*)"', 2) as game_start_time
                    , cast(concat(game_start_date, ' ', game_start_time) as timestamp) as game_start_timestamp
                    , cast(end_time as timestamp) as game_end_timestamp
                    , age(game_end_timestamp, game_start_timestamp) as time_played_interval
                    , epoch(time_played_interval) as time_played_seconds
                    , *
                    from player_games
                )
                select * from final
            );
        """)


@asset(deps=[dlt_chess_players_games], group_name="prep")
def game_moves(duckdb: DuckDBResource):
    def _get_game_fens(game_move_index: int, pgn_string: str) -> str:
        pgn_parsed = StringIO(pgn_string)
        game = chess.pgn.read_game(pgn_parsed)
        board = game.board()
        
        i = 1
        for move in game.mainline_moves():
            board.push(move)
            if i == game_move_index:
                break
            i += 1
        
        return board.fen()
    
    with duckdb.get_connection() as conn:
        conn.sql("SET TimeZone = 'UTC';")
        df: pd.DataFrame = conn.sql("""
                with player_games as (
                    select
                    uuid
                    , time_control
                    , pgn
                    from chess_data_raw.players_games
                )
                , base as (
                    select
                    uuid
                    , time_control
                    , cast(split(time_control, '+')[1] as integer) as time_control_start
                    , cast(coalesce(split(time_control, '+')[2], '0') as integer) as time_control_add
                    , pgn
                    , split(pgn, '\n\n')[2] as pgn_moves
                    , regexp_extract_all(pgn_moves, '\d+\.+ [\S]+ {\[%clk \S+\]}') as moves_extract
                    from player_games
                )
                , unnest as (
                    select
                    uuid
                    , pgn
                    , time_control
                    , time_control_start
                    , time_control_add
                    , unnest(moves_extract) as moves_unnest
                    , generate_subscripts(moves_extract, 1) AS game_move_index
                    , split(moves_unnest, ' ')[1] as color_move_index_raw
                    , cast(regexp_replace(color_move_index_raw, '\.+', '') as int) as color_move_index
                    , if(regexp_matches(color_move_index_raw, '\.\.\.'), 'Black', 'White') as color_move
                    , split(moves_unnest, ' ')[2] as move
                    , cast(replace(split(moves_unnest, ' ')[4], ']}', '') as interval) as clock_interval
                    , to_seconds(epoch(clock_interval) + time_control_add) as clock_interval_post_move
                    from base
                )
                , final as (
                    select 
                    uuid
                    , pgn
                    , time_control
                    , time_control_add
                    , time_control_start
                    , game_move_index
                    , color_move
                    , color_move_index
                    , move
                    , clock_interval
                    , clock_interval_post_move
                    , coalesce(
                        lag(clock_interval_post_move) over(partition by uuid, color_move order by color_move_index)
                        , to_seconds(time_control_start)
                    )  as prev_clock_interval
                    , epoch(prev_clock_interval) - epoch(clock_interval)as move_time
                    from unnest
                )
                select * from final
        """).to_df()
        
        df['game_move_fen'] = df[['game_move_index', 'pgn']].apply(lambda x: _get_game_fens(x['game_move_index'], x['pgn']), axis=1)
        
        conn.sql("""
            CREATE SCHEMA IF NOT EXISTS chess_data_prep;
            CREATE OR REPLACE TABLE chess_data_prep.game_moves as (
                select * from df
            )
        """)
        
# @asset(deps=[game_moves], group_name="prep")
# def game_moves_centipawn(duckdb: DuckDBResource):
#     # https://python-chess.readthedocs.io/en/latest/engine.html#chess.engine.Score
#     async def process_fen(uuid_index_fen):
#         uuid, move_index, fen = uuid_index_fen
        
#         transport, engine = await chess.engine.popen_uci("/opt/homebrew/bin/stockfish")
#         board = chess.Board(fen=fen)
#         info = await engine.analyse(board, chess.engine.Limit(time=0.1))
#         score = info["score"].white().score()
#         await engine.quit()
        
#         return [uuid, move_index, score]
    
#     async def process_data():        
#         with duckdb.get_connection() as conn:
#             uuid_index_fen = conn.sql("""select
#                           uuid
#                           , game_move_index
#                           , game_move_fen
#                           from chess_data_prep.game_moves"""
#                           ).to_df().values.tolist()
            
#             res = await asyncio.gather(*map(process_fen, uuid_index_fen))
#             df = pd.DataFrame(res, columns=['uuid', 'game_move_index', 'centipawn_score'])
            
#             conn.sql("""
#                 SET TimeZone = 'UTC';
#                 CREATE SCHEMA IF NOT EXISTS chess_data_prep;
#                 CREATE OR REPLACE TABLE chess_data_prep.game_moves_centipawn as (
#                     select * from df
#                 )
#             """)
    
#     asyncio.run(process_data())