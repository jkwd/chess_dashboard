from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
)
from chess_etl.assets import chess_source, asset_checks
from chess_etl.assets.staging import players_games
from chess_etl.assets.prep import game_moves
from chess_etl.assets.core import player_games
from chess_etl.resources import dlt_resource, duckdb_resource

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *"
)

# Asset
chess_source_assets = load_assets_from_modules([chess_source])
chess_staging_assets = load_assets_from_modules([players_games])
chess_prep_assets = load_assets_from_modules([game_moves])
chess_core_assets = load_assets_from_modules([player_games])


# Strict Asset Checks
all_asset_checks = []
for check_blob in players_games.players_games_check_blobs:
    all_asset_checks.append(asset_checks.make_check(check_blob))

for check_blob in game_moves.game_moves_check_blobs:
    all_asset_checks.append(asset_checks.make_check(check_blob))

# Approx Asset Checks
for check_blob in game_moves.game_moves_approx_check_blobs:
    all_asset_checks.append(asset_checks.make_perc_approx_check(check_blob))


# Must be last
defs = Definitions(
    assets=[*chess_source_assets, *chess_staging_assets, *chess_prep_assets, *chess_core_assets],
    asset_checks=all_asset_checks,
    resources={
        "dlt": dlt_resource,
        "duckdb": duckdb_resource,
    },
    schedules=[daily_refresh_schedule],
)