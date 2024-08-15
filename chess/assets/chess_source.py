from dagster import AssetExecutionContext
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets
from dlt import pipeline, destinations
from dlt_sources.chess import source

from . import constants

# https://docs.dagster.io/integrations/embedded-elt/dlt

@dlt_assets(
    dlt_source=source(
        # players=['johnnywhoopp'], start_month="2022/11", end_month="2022/12"
        players=['johnnywhoopp']
    ),
    dlt_pipeline = pipeline(
        pipeline_name="chess_pipeline",
        destination=destinations.duckdb(constants.CHESS_DB),
        dataset_name="chess_data_raw",
    ),
    name="chess",
    group_name="ingestion",
)
def dagster_chess_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)