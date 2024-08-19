from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
    asset_check,
    AssetChecksDefinition,
    AssetCheckResult,
)
from chess_etl.assets import chess_source, chess_games
from chess_etl.resources import dlt_resource, duckdb_resource

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


daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *"
)

# Asset Checks
asset_check_blobs = []
asset_check_blobs.extend(chess_source.source_check_blobs)

chess_source_assets = load_assets_from_modules([chess_source])
chess_games_assets = load_assets_from_modules([chess_games])

# Must be last
defs = Definitions(
    assets=[*chess_source_assets, *chess_games_assets],
    asset_checks=[make_check(check_blob) for check_blob in asset_check_blobs],
    resources={
        "dlt": dlt_resource,
        "duckdb": duckdb_resource,
    },
    schedules=[daily_refresh_schedule],
)