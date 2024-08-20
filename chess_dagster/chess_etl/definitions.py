from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
)
from chess_etl.assets import chess_source, chess_games, asset_checks
from chess_etl.resources import dlt_resource, duckdb_resource

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *"
)

# Asset Checks
asset_check_blobs = []
asset_check_blobs.extend(asset_checks.source_check_blobs)

chess_source_assets = load_assets_from_modules([chess_source])
chess_games_assets = load_assets_from_modules([chess_games])

# Must be last
defs = Definitions(
    assets=[*chess_source_assets, *chess_games_assets],
    asset_checks=[asset_checks.make_check(check_blob) for check_blob in asset_check_blobs],
    resources={
        "dlt": dlt_resource,
        "duckdb": duckdb_resource,
    },
    schedules=[daily_refresh_schedule],
)