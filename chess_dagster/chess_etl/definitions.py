from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
)
from chess_etl.assets_dlt import chess_dlt_assets
from chess_etl.assets_dbt import chess_dbt_assets
from chess_etl.resources import dlt_resource, dbt_resource


daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *"
)

# Must be last
defs = Definitions(
    assets=[chess_dlt_assets, chess_dbt_assets],
    resources={
        "dlt": dlt_resource,
        "dbt": dbt_resource,
    },
    schedules=[daily_refresh_schedule],
)
