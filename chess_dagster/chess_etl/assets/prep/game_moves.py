from dagster import AssetKey, AssetSpec, asset
from dagster_duckdb import DuckDBResource
from ..constants import SCHEMA_STAGING, SCHEMA_PREP

import pandas as pd
import os

players_games = AssetSpec(AssetKey("players_games"))
table_name, _ = os.path.splitext(os.path.basename(__file__))

@asset(deps=[players_games], group_name='prep')
def game_moves(duckdb: DuckDBResource):
    # def _get_game_fens(game_move_index: int, pgn_string: str) -> str:
    #     pgn_parsed = StringIO(pgn_string)
    #     game = chess.pgn.read_game(pgn_parsed)
    #     board = game.board()
        
    #     i = 1
    #     for move in game.mainline_moves():
    #         board.push(move)
    #         if i == game_move_index:
    #             break
    #         i += 1
        
    #     return board.fen()
    
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
                    , cast(split(time_control, '+')[1] as integer) as time_control_base
                    , cast(coalesce(split(time_control, '+')[2], '0') as integer) as time_control_add_seconds
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
                    , time_control_base
                    , time_control_add_seconds
                    , unnest(moves_extract) as moves_unnest
                    , generate_subscripts(moves_extract, 1) AS game_move_index
                    , split(moves_unnest, ' ')[1] as color_move_index_raw
                    , cast(regexp_replace(color_move_index_raw, '\.+', '') as int) as color_move_index
                    , if(regexp_matches(color_move_index_raw, '\.\.\.'), 'Black', 'White') as color_move
                    , split(moves_unnest, ' ')[2] as move

                    -- This is the clock after the addition of time
                    , epoch(cast(replace(split(moves_unnest, ' ')[4], ']}', '') as interval)) as clock_interval_post_move

                    -- To get the clock before the addition of time
                    , clock_interval_post_move - time_control_add_seconds as clock_interval_move
                    from base
                )
                , final as (
                    select 
                    uuid
                    , pgn
                    , time_control
                    , time_control_base
                    , time_control_add_seconds
                    , game_move_index
                    , color_move
                    , color_move_index
                    , move
                    , coalesce(
                        lag(clock_interval_post_move) over(partition by uuid, color_move order by color_move_index)
                        , time_control_base
                    )  as prev_clock_interval
                    , clock_interval_move
                    , clock_interval_post_move
                    , prev_clock_interval - clock_interval_move as move_time_seconds
                    from unnest
                )
                select
                concat(uuid::string, '_', game_move_index::string) as id
                , uuid::string as uuid
                , pgn::string as pgn
                , time_control::string as time_control
                , time_control_base::int as time_control_base
                , time_control_add_seconds::int as time_control_add_seconds
                , game_move_index::int as game_move_index
                , color_move::string as color_move
                , color_move_index::int as color_move_index
                , move::string as move
                , prev_clock_interval::double as prev_clock_interval
                , clock_interval_move::double as clock_interval_move
                , clock_interval_post_move::double as clock_interval_post_move
                , move_time_seconds::double as move_time_seconds
                from final
        """).to_df()
        
        # df['game_move_fen'] = df[['game_move_index', 'pgn']].apply(lambda x: _get_game_fens(x['game_move_index'], x['pgn']), axis=1)
        
        conn.sql(f'CREATE SCHEMA IF NOT EXISTS {SCHEMA_PREP};')
        conn.sql(f"""
            CREATE OR REPLACE TABLE {SCHEMA_PREP}.{table_name} as (
                select * from df
            )
        """)
    conn.close()


game_moves_check_blobs = [
    {
        "name": "game_moves__id__is_unique",
        "asset": table_name,
        "sql": f"""
            select
            id
            , count(1) as cnt
            from {SCHEMA_PREP}.{table_name}
            group by 1
            having count(1) > 1
        """,
    },
    {
        "name": "game_moves__color_move_index__has_no_nulls",
        "asset": table_name,
        "sql": f"""
            select
            color_move_index
            from {SCHEMA_PREP}.{table_name}
            where color_move_index is null
        """,
    },
    {
        "name": "game_moves__move_time__has_no_nulls",
        "asset": table_name,
        "sql": f"""
            select
            move_time_seconds
            from {SCHEMA_PREP}.{table_name}
            where move_time_seconds is null
        """,
    },
]

game_moves_approx_check_blobs = [
    {
        "name": "game_moves__move_time__is_positive",
        "asset": table_name,
        "sql": f"""
            select 
            count_if(move_time_seconds < 0) as neg_time
            , count(1) as num_rows 
            , count_if(move_time_seconds < 0) / count(1) * 100.0 as perc
            from {SCHEMA_PREP}.{table_name}
        """,
    },
]