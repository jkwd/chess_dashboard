from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules
)
from .assets import chess_source, chess_games
from .resources import dlt_resource, duckdb_resource

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *"
)

chess_source = load_assets_from_modules([chess_source])
chess_games = load_assets_from_modules([chess_games])

# Must be last
defs = Definitions(
    assets=[*chess_source, *chess_games],
    resources={
        "dlt": dlt_resource,
        "duckdb": duckdb_resource,
    },
    schedules=[daily_refresh_schedule],
)