from dagster_embedded_elt.dlt import DagsterDltResource
from dagster_duckdb import DuckDBResource
from dagster_dbt import DbtCliResource

from chess_etl.assets.constants import CHESS_DB
from pathlib import Path
import os

HOME_DIR = os.getenv("HOME")

dlt_resource = DagsterDltResource()
duckdb_resource = DuckDBResource(database=CHESS_DB)

dbt_project_dir = Path(__file__).joinpath("..", "..", "chess_dbt").resolve()
dbt_resource = DbtCliResource(project_dir=os.fspath(dbt_project_dir),
                              profiles_dir=os.path.join(HOME_DIR, ".dbt"),
                              global_config_flags=["--log-format-file", "text"],
                              target="prod")

# If DAGSTER_DBT_PARSE_PROJECT_ON_LOAD is set, a manifest will be created at run time.
# Otherwise, we expect a manifest to be present in the project's target directory.
if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
    dbt_manifest_path = (
        dbt_resource.cli(
            ["--quiet", "parse"],
            target_path=Path("target"),
        )
        .wait()
        .target_path.joinpath("manifest.json")
    )
else:
    dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")
