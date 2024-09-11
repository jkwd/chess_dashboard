from dagster import AssetKey, AssetSpec, asset
from dagster_duckdb import DuckDBResource

import os
import pandas as pd
import chess
import chess.pgn
import chess.engine
from ..constants import SCHEMA_CORE

username: str = os.getenv("USERNAME")
game_moves = AssetSpec(AssetKey("game_moves"))
table_name, _ = os.path.splitext(os.path.basename(__file__))

def get_checkmate_pieces(fen, player_color, player_result, opponent_result):
    if not (player_result == 'checkmated' or opponent_result == 'checkmated'):
        return []
    
    board = chess.Board(fen)

    if not board.is_checkmate():
        return []
    
    if player_color == 'White':
        if player_result == 'win':
            winning_color = chess.WHITE
            checkmated_color = chess.BLACK
        else:
            winning_color = chess.BLACK
            checkmated_color = chess.WHITE
    else:
        if player_result == 'win':
            winning_color = chess.BLACK
            checkmated_color = chess.WHITE
        else:
            winning_color = chess.WHITE
            checkmated_color = chess.BLACK

    

    # Get position of Checkmated King 
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.KING and piece.color == checkmated_color:
            king_square = square
            break

    # Get possible moves by king
    official_king_moves = board.attacks(king_square)
    attacked_squares = [king_square]
    for square in official_king_moves:
        piece = board.piece_at(square)
    
        if not piece or piece.color != checkmated_color:
            attacked_squares.append(square)

    # Get attacking pieces
    attacking_pieces = []
    for square in attacked_squares:
        attacker_ids = list(board.attackers(color=winning_color, square=square))
        attacking_pieces.extend(attacker_ids)
    attacking_pieces = set(attacking_pieces) # dedup the board pieces based on position

    return sorted([chess.piece_name(board.piece_at(attacker).piece_type) for attacker in attacking_pieces])

@asset(deps=[game_moves], group_name='core')
def player_games(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.sql("SET TimeZone = 'UTC';")
        df: pd.DataFrame = conn.sql(f"""
            with game_moves_pivot as (
                PIVOT chess_data_prep.game_moves
                ON color_move
                USING sum(move_time_seconds) as total_move_time, count(1) as num_moves
                group by uuid
            )
            , game_moves as (
                select
                uuid
                , white_total_move_time
                , white_num_moves
                , black_total_move_time
                , black_num_moves
                from game_moves_pivot
            )
            , player_games as (
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
            , joined as (
                select
                pg.*
                , white_total_move_time
                , white_num_moves
                , black_total_move_time
                , black_num_moves
                from player_games as pg
                left join game_moves as gm
                on pg.uuid = gm.uuid
            )
            , final as (
                select
                -- PLAYER DETAILS
                if(lower(white__username)='{username}', 'White', 'Black') as player_color
                , if(player_color = 'White', white__rating, black__rating) as player_rating
                , if(player_color = 'White', white__result, black__result) as player_result
                , if(player_color = 'White', white_total_move_time, black_total_move_time) as player_total_move_time
                , if(player_color = 'White', white_num_moves, black_num_moves) as player_num_moves

                -- OPPONENT DETAILS
                , if(player_color = 'White', black__rating, white__rating) as opponent_rating
                , if(player_color = 'White', black__result, white__result) as opponent_result
                , if(player_color = 'White', black_total_move_time, white_total_move_time) as opponent_total_move_time
                , if(player_color = 'White', black_num_moves, white_num_moves) as opponent_num_moves

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

                -- ECO DETAILS
                , regexp_extract(pgn, '(ECO )"(.*)"', 2) as eco
                , regexp_extract(pgn, '(ECOUrl )"(.*)"', 2) as eco_url
                , replace(eco_url, 'https://www.chess.com/openings/', '') as eco_name
                
                -- GAME TIME DETAILS
                , cast(replace(regexp_extract(pgn, '(UTCDate )"(.*)"', 2), '.', '-') as date) as game_start_date
                , regexp_extract(pgn, '(StartTime )"(.*)"', 2) as game_start_time
                , cast(concat(game_start_date, ' ', game_start_time) as timestamp) as game_start_timestamp
                , cast(end_time as timestamp) as game_end_timestamp
                , age(game_end_timestamp, game_start_timestamp) as time_played_interval
                , epoch(time_played_interval) as time_played_seconds
                , *
                from joined
            )
            select * from final
        """).to_df()
        
        df['checkmate_pieces'] = df[['fen', 'player_color', 'player_result', 'opponent_result']].apply(lambda x: get_checkmate_pieces(x.fen, x.player_color, x.player_result, x.opponent_result), axis=1)
        
        conn.sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_CORE};")
        conn.sql(f"""
            CREATE OR REPLACE TABLE {SCHEMA_CORE}.{table_name} as (
                select * from df
            );
        """)

    conn.close()