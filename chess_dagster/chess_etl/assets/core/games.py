from dagster import AssetKey, AssetSpec, asset
from dagster_duckdb import DuckDBResource

import os
import pandas as pd
import chess
import chess.pgn
import chess.engine
from chess_etl.assets.constants import SCHEMA_CORE, PREP_GAME_MOVES, PREP_PLAYER_GAMES, CORE_PLAYER_GAMES

game_moves = AssetSpec(AssetKey("game_moves"))
prep_player_games = AssetSpec(AssetKey("prep_player_games"))


@asset(deps=[game_moves, prep_player_games], group_name='core')
def games(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.sql("SET TimeZone = 'UTC';")
        conn.sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_CORE};")
        conn.sql(f"""
            CREATE OR REPLACE TABLE {CORE_PLAYER_GAMES} as (
                with game_moves_pivot as (
                    PIVOT {PREP_GAME_MOVES}
                    ON color_move
                    USING sum(move_time_seconds) as total_move_time, count(1) as num_moves
                    group by uuid
                )
                , player_games as (
                    select *
                    from {PREP_PLAYER_GAMES}
                )
                , joined as (
                    select
                    pg.*
                    , white_total_move_time
                    , white_num_moves
                    , black_total_move_time
                    , black_num_moves
                    from player_games as pg
                    
                    left join game_moves_pivot as gm
                    on pg.uuid = gm.uuid
                )
                , final as (
                    select
                    *

                    -- PLAYER DETAILS
                    , if(player_color = 'White', white_total_move_time, black_total_move_time) as player_total_move_time
                    , if(player_color = 'White', white_num_moves, black_num_moves) as player_num_moves

                    -- OPPONENT DETAILS
                    , if(player_color = 'White', black_total_move_time, white_total_move_time) as opponent_total_move_time
                    , if(player_color = 'White', black_num_moves, white_num_moves) as opponent_num_moves

                    -- GAME TIME DETAILS
                    , cast(replace(regexp_extract(pgn, '(UTCDate )"(.*)"', 2), '.', '-') as date) as game_start_date
                    , regexp_extract(pgn, '(StartTime )"(.*)"', 2) as game_start_time
                    , cast(concat(game_start_date, ' ', game_start_time) as timestamp) as game_start_timestamp
                    , cast(end_time as timestamp) as game_end_timestamp
                    , age(game_end_timestamp, game_start_timestamp) as time_played_interval
                    , epoch(time_played_interval) as time_played_seconds

                    from joined
                )
                select
                -- ID
                uuid

                -- GAME
                , url
                , rated
                , rules
                , time_class

                -- TIME
                , time_control
                , time_control_base
                , time_control_add_seconds
                , time_played_seconds
                , game_start_timestamp
                , game_end_timestamp

                -- WHITE-BLACK
                , white__uuid
                , white__username
                , white__aid
                , white__rating
                , white__result
                , white_total_move_time
                , white_num_moves

                , black__uuid
                , black__username
                , black__aid
                , black__rating
                , black__result
                , black_total_move_time
                , black_num_moves

                -- PLAYER-OPPONENT
                , player_color
                , player_rating
                , player_result
                , player_total_move_time
                , player_num_moves
                , opponent_rating
                , opponent_result
                , opponent_total_move_time
                , opponent_num_moves
                , is_stronger_opponent
                , player_wdl
                , player_wdl_reason

                -- BOARD
                , initial_setup
                , fen
                , pgn
                , pgn_moves
                , pgn_move_extract
                , pgn_clock_extract
                , eco
                , eco_url
                , eco_name
                , checkmate_pieces

                -- MISC
                , tcn
                , accuracies__white
                , accuracies__black

                from final
            )
        """)
    conn.close()
    
games_check_blobs = [
    {
        "name": "games__player_num_moves__positive",
        "asset": games,
        "sql": f"""
            select
            uuid
            from {CORE_PLAYER_GAMES}
            where player_num_moves < 0
            group by 1
        """,
    },
]