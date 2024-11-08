import os
from . import constants

from dagster import AssetExecutionContext
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets
from dlt import pipeline, destinations
from chess_dlt.chess import source


# https://docs.dagster.io/integrations/embedded-elt/dlt

@dlt_assets(
    dlt_source=source(
        # username='magnuscarlsen'
        username=os.getenv("USERNAME")
    ),
    dlt_pipeline=pipeline(
        pipeline_name="chess_pipeline",
        destination=destinations.duckdb(constants.CHESS_DB),
        dataset_name=constants.SCHEMA_RAW,
    ),
    name="chess",
)
def dagster_chess_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)
