from dagster import (
    asset_check,
    AssetChecksDefinition,
    AssetCheckResult,
)

from typing import Mapping

# https://docs.dagster.io/concepts/assets/asset-checks/define-execute-asset-checks
def make_check(check_blob: Mapping[str, str]) -> AssetChecksDefinition:
    @asset_check(
        name=check_blob["name"],
        asset=check_blob["asset"],
        required_resource_keys={"duckdb"},
        blocking=True
    )
    def _check(context):
        with context.resources.duckdb.get_connection() as conn:
            conn.sql("SET TimeZone = 'UTC';")
            rows = conn.sql(check_blob["sql"]).to_df()
        conn.close()
        return AssetCheckResult(passed=len(rows) == 0, metadata={"num_rows": len(rows)})

    return _check

players_games_raw = 'chess_data_raw.players_games'
source_check_blobs = [
    {
        "name": "uuid_has_no_nulls",
        "asset": "dlt_chess_players_games",
        "sql": f"""
            select * 
            from {players_games_raw} 
            where uuid is null
            or uuid = ''
        """,
    },
    {
        "name": "uuid_is_unique",
        "asset": "dlt_chess_players_games",
        "sql": f"""
            select
            uuid
            , count(1) as cnt
            from {players_games_raw} 
            group by uuid
            having count(1) > 1
        """,
    },
    {
        "name": "time_control_has_no_nulls",
        "asset": "dlt_chess_players_games",
        "sql": f"""
            select * 
            from {players_games_raw} 
            where time_control is null
            or time_control = ''
        """,
    },
    {
        "name": "white__username_has_no_nulls",
        "asset": "dlt_chess_players_games",
        "sql": f"""
            select * 
            from {players_games_raw} 
            where white__username is null
            or white__username = ''
        """,
    },
    {
        "name": "black__username_has_no_nulls",
        "asset": "dlt_chess_players_games",
        "sql": f"""
            select * 
            from {players_games_raw} 
            where black__username is null
            or black__username = ''
        """,
    },
    {
        "name": "white__resulte_has_no_nulls",
        "asset": "dlt_chess_players_games",
        "sql": f"""
            select * 
            from {players_games_raw} 
            where white__result is null
            or white__result = ''
        """,
    },
    {
        "name": "black__result_has_no_nulls",
        "asset": "dlt_chess_players_games",
        "sql": f"""
            select * 
            from {players_games_raw} 
            where black__result is null
            or black__result = ''
        """,
    },
]