from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
)
from chess_etl.assets.dlt_assets import dagster_chess_assets
from chess_etl.assets.dbt_assets import chess_dbt_dbt_assets
# from chess_etl.assets.prep import prep_player_games
# from chess_etl.assets.core import games
from chess_etl.resources import dlt_resource, duckdb_resource, dbt_resource


daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *"
)

# Asset
# dlt_chess_players_games_assets = load_assets_from_modules([dlt_chess_players_games])
# prep_player_games_assets = load_assets_from_modules([prep_player_games])
# chess_core_assets = load_assets_from_modules([games])
# import_dbt_assets = load_assets_from_modules([dbt_assets])


# Strict Asset Checks
all_asset_checks = []

# for check_blob in prep_player_games.prep_player_games_check_blobs:
#     all_asset_checks.append(asset_checks.make_check(check_blob))

# for check_blob in games.games_check_blobs:
#     all_asset_checks.append(asset_checks.make_check(check_blob))

# Must be last
defs = Definitions(
    assets=[dagster_chess_assets, chess_dbt_dbt_assets],
    resources={
        "dlt": dlt_resource,
        "duckdb": duckdb_resource,
        "dbt": dbt_resource,
    },
    schedules=[daily_refresh_schedule],
)
