from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from chess_etl.resources import dbt_manifest_path


@dbt_assets(manifest=dbt_manifest_path)
def chess_dbt_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
