from dagster import AssetKey, AssetSpec, asset, asset_check, AssetCheckResult
from dagster_duckdb import DuckDBResource
from ..constants import SCHEMA_RAW, SCHEMA_STAGING

import os

dlt_chess_players_games = AssetSpec(AssetKey("dlt_chess_players_games"))
table_name, _ = os.path.splitext(os.path.basename(__file__))

@asset(deps=[dlt_chess_players_games], group_name='staging')
def players_games(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.sql("SET TimeZone = 'UTC';")
        conn.sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_STAGING};")
        conn.sql(f"""
                CREATE OR REPLACE VIEW {SCHEMA_STAGING}.{table_name} as (
                    select
                    end_time::timestamp as end_time
                    , url::string as url
                    , pgn::string as pgn
                    , time_control:: string as time_control
                    , rated::boolean as rated
                    , accuracies__white::double as accuracies__white
                    , accuracies__black::double as accuracies__black
                    , tcn::string as tcn
                    , uuid::string as uuid
                    , initial_setup::string as initial_setup
                    , fen::string as fen
                    , time_class::string as time_class
                    , rules::string as rules
                    , white__rating::int as white__rating
                    , white__result::string as white__result
                    , white__aid::string as white__aid
                    , white__username::string as white__username
                    , white__uuid::string as white__uuid
                    , black__rating::int as black__rating
                    , black__result::string as black__result
                    , black__aid::string as black__aid
                    , black__username::string as black__username
                    , black__uuid::string as black__uuid
                    , _dlt_load_id::double as _dlt_load_id
                    , _dlt_id::string as _dlt_id
                    , tournament::string as tournament
                    from {SCHEMA_RAW}.{table_name}
                )
                 """)
    conn.close()

players_games_check_blobs = [
    {
        "name": "players_games__uuid__has_no_nulls",
        "asset": players_games,
        "sql": f"""
            select * 
            from {SCHEMA_STAGING}.{table_name}
            where uuid is null
            or uuid = ''
        """,
    },
    {
        "name": "players_games__uuid__is_unique",
        "asset": players_games,
        "sql": f"""
            select
            uuid
            , count(1) as cnt
            from {SCHEMA_STAGING}.{table_name}
            group by uuid
            having count(1) > 1
        """,
    },
    {
        "name": "players_games__time_control__has_no_nulls",
        "asset": players_games,
        "sql": f"""
            select * 
            from {SCHEMA_STAGING}.{table_name} 
            where time_control is null
            or time_control = ''
        """,
    },
    {
        "name": "players_games__white__username__has_no_nulls",
        "asset": players_games,
        "sql": f"""
            select * 
            from {SCHEMA_STAGING}.{table_name} 
            where white__username is null
            or white__username = ''
        """,
    },
    {
        "name": "players_games__black__username__has_no_nulls",
        "asset": players_games,
        "sql": f"""
            select * 
            from {SCHEMA_STAGING}.{table_name} 
            where black__username is null
            or black__username = ''
        """,
    },
    {
        "name": "players_games__white__resulte__has_no_nulls",
        "asset": players_games,
        "sql": f"""
            select * 
            from {SCHEMA_STAGING}.{table_name} 
            where white__result is null
            or white__result = ''
        """,
    },
    {
        "name": "players_games__black__result__has_no_nulls",
        "asset": players_games,
        "sql": f"""
            select * 
            from {SCHEMA_STAGING}.{table_name} 
            where black__result is null
            or black__result = ''
        """,
    },
]