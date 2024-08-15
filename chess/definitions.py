from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules
)
from .assets import chess
from .resources import dlt_resource

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *"
)

chess_assets = load_assets_from_modules([chess])

# Must be last
defs = Definitions(
    assets=[*chess_assets],
    resources={
        "dlt": dlt_resource,
    },
    schedules=[daily_refresh_schedule],
)