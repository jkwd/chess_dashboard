from dagster import AssetKey, AssetSpec, asset
from dagster_duckdb import DuckDBResource

dlt_chess_players_games = AssetSpec(AssetKey("dlt_chess_players_games"))

@asset(deps=[dlt_chess_players_games], group_name="prep")
def my_table(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.execute("create view test as (select * from chess_data_raw.players_games limit 5)")