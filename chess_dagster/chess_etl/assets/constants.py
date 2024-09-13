# STOCKFISH_PATH = "/usr/games/stockfish" # Docker
# STOCKFISH_PATH = "/opt/homebrew/bin/stockfish" # MAC
CHESS_DB = '/data/chess.duckdb'

# Table names
# Schema
SCHEMA_RAW = 'chess_data_raw'
SCHEMA_STAGING = 'chess_data_staging'
SCHEMA_PREP = 'chess_data_prep'
SCHEMA_CORE = 'chess_data_core'


# Tables
RAW_PLAYERS_GAME = f'{SCHEMA_RAW}.players_games'
STAGING_PLAYERS_GAME = f'{SCHEMA_STAGING}.players_games'
PREP_PLAYER_GAMES = f'{SCHEMA_PREP}.player_games'
PREP_GAME_MOVES = f'{SCHEMA_PREP}.game_moves'
CORE_PLAYER_GAMES = f'{SCHEMA_CORE}.games'
