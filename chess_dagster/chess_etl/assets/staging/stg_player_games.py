from dagster import AssetKey, AssetSpec, asset
from dagster_duckdb import DuckDBResource
from chess_etl.assets.constants import SCHEMA_STAGING, RAW_PLAYERS_GAME, STAGING_PLAYERS_GAME

dlt_chess_players_games = AssetSpec(AssetKey("dlt_chess_players_games"))


@asset(deps=[dlt_chess_players_games], group_name='staging')
def stg_player_games(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.sql("SET TimeZone = 'UTC';")
        conn.sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_STAGING};")
        conn.sql(f"""
                CREATE OR REPLACE VIEW {STAGING_PLAYERS_GAME} as (
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
                    from {RAW_PLAYERS_GAME}
                )
        """)
    conn.close()


players_games_check_blobs = [
    {
        "name": "uuid__has_no_nulls",
        "asset": stg_player_games,
        "sql": f"""
            select *
            from {STAGING_PLAYERS_GAME}
            where uuid is null
            or uuid = ''
        """,
    },
    {
        "name": "uuid__is_unique",
        "asset": stg_player_games,
        "sql": f"""
            select
            uuid
            , count(1) as cnt
            from {STAGING_PLAYERS_GAME}
            group by uuid
            having count(1) > 1
        """,
    },
    {
        "name": "time_control__has_no_nulls",
        "asset": stg_player_games,
        "sql": f"""
            select *
            from {STAGING_PLAYERS_GAME}
            where time_control is null
            or time_control = ''
        """,
    },
    {
        "name": "white__username__has_no_nulls",
        "asset": stg_player_games,
        "sql": f"""
            select *
            from {STAGING_PLAYERS_GAME}
            where white__username is null
            or white__username = ''
        """,
    },
    {
        "name": "black__username__has_no_nulls",
        "asset": stg_player_games,
        "sql": f"""
            select *
            from {STAGING_PLAYERS_GAME}
            where black__username is null
            or black__username = ''
        """,
    },
    {
        "name": "white__resulte__has_no_nulls",
        "asset": stg_player_games,
        "sql": f"""
            select *
            from {STAGING_PLAYERS_GAME}
            where white__result is null
            or white__result = ''
        """,
    },
    {
        "name": "black__result__has_no_nulls",
        "asset": stg_player_games,
        "sql": f"""
            select *
            from {STAGING_PLAYERS_GAME}
            where black__result is null
            or black__result = ''
        """,
    },
]
