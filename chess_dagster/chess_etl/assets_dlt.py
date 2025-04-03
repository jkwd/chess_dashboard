import os
from chess_etl.constants import SCHEMA_RAW

from dagster import AssetExecutionContext
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets
from dlt import pipeline, destinations
from chess_dlt import source


# https://docs.dagster.io/integrations/embedded-elt/dlt

@dlt_assets(
    dlt_source=source(
        username=os.getenv("CHESS_USERNAME")
    ),
    dlt_pipeline=pipeline(
        pipeline_name="chess_pipeline",
        destination=destinations.duckdb(os.getenv('CHESS_DB')),
        dataset_name=SCHEMA_RAW, # This is the table schema in duckdb.
    ),
    name="chess", # This is the table catalog in duckdb.
)
def chess_dlt_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)
