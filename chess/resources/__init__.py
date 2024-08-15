from dagster_embedded_elt.dlt import DagsterDltResource
from dagster_duckdb import DuckDBResource
from ..assets.constants import CHESS_DB

dlt_resource = DagsterDltResource()
duckdb_resource = DuckDBResource(database=CHESS_DB)