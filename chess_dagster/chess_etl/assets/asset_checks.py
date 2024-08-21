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
players_games_raw_asset = 'dlt_chess_players_games'

game_moves = 'chess_data_prep.game_moves'
game_moves_asset = 'game_moves'

player_games_core = 'chess_data_core.player_games'
player_games_core_asset = 'player_games'

source_check_blobs = [
    {
        "name": "uuid__has_no_nulls",
        "asset": players_games_raw_asset,
        "sql": f"""
            select * 
            from {players_games_raw} 
            where uuid is null
            or uuid = ''
        """,
    },
    {
        "name": "uuid__is_unique",
        "asset": players_games_raw_asset,
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
        "name": "time_control__has_no_nulls",
        "asset": players_games_raw_asset,
        "sql": f"""
            select * 
            from {players_games_raw} 
            where time_control is null
            or time_control = ''
        """,
    },
    {
        "name": "white__username__has_no_nulls",
        "asset": players_games_raw_asset,
        "sql": f"""
            select * 
            from {players_games_raw} 
            where white__username is null
            or white__username = ''
        """,
    },
    {
        "name": "black__username__has_no_nulls",
        "asset": players_games_raw_asset,
        "sql": f"""
            select * 
            from {players_games_raw} 
            where black__username is null
            or black__username = ''
        """,
    },
    {
        "name": "white__resulte__has_no_nulls",
        "asset": players_games_raw_asset,
        "sql": f"""
            select * 
            from {players_games_raw} 
            where white__result is null
            or white__result = ''
        """,
    },
    {
        "name": "black__result__has_no_nulls",
        "asset": players_games_raw_asset,
        "sql": f"""
            select * 
            from {players_games_raw} 
            where black__result is null
            or black__result = ''
        """,
    },
]


game_moves_check_blobs = [
    {
        "name": "color_move_index__has_no_nulls",
        "asset": game_moves_asset,
        "sql": f"""
            select
            color_move_index
            from {game_moves} 
            where color_move_index is null
        """,
    },
    {
        "name": "move_time__has_no_nulls",
        "asset": game_moves_asset,
        "sql": f"""
            select
            move_time_seconds
            from {game_moves} 
            where move_time_seconds is null
        """,
    },
    {
        "name": "move_time__is_positive",
        "asset": game_moves_asset,
        "sql": f"""
            select
            move_time_seconds
            from {game_moves} 
            where move_time_seconds < 0
        """,
    },
]