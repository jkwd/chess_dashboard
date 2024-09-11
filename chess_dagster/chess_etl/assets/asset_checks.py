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
        blocking=check_blob['blocking'] if 'blocking' in check_blob else True
    )
    def _check(context):
        with context.resources.duckdb.get_connection() as conn:
            conn.sql("SET TimeZone = 'UTC';")
            rows = conn.sql(check_blob["sql"]).to_df()
        conn.close()
        return AssetCheckResult(passed=len(rows) == 0, metadata={"num_rows": len(rows)})

    return _check

def make_perc_approx_check(check_blob: Mapping[str, str]) -> AssetChecksDefinition:
    @asset_check(
        name=check_blob["name"],
        asset=check_blob["asset"],
        required_resource_keys={"duckdb"},
        blocking=check_blob['blocking'] if 'blocking' in check_blob else True
    )
    def _check(context):
        with context.resources.duckdb.get_connection() as conn:
            conn.sql("SET TimeZone = 'UTC';")
            df = conn.sql(check_blob["sql"]).to_df()
        conn.close()
        
        perc = df.iloc[0]['perc'].item()
        threshold = check_blob['threshold']
        
        return AssetCheckResult(passed=perc < threshold, metadata={"perc": perc})

    return _check