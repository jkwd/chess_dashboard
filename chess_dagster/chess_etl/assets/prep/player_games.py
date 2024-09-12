from dagster import AssetKey, AssetSpec, asset
from dagster_duckdb import DuckDBResource

import chess

import os
from ..constants import SCHEMA_PREP, STAGING_PLAYERS_GAME, PREP_PLAYER_GAMES

username: str = os.getenv("USERNAME")
staging_players_games = AssetSpec(AssetKey("players_games"))

def get_checkmate_pieces(fen, player_color, player_result, opponent_result):
    if not (player_result == 'checkmated' or opponent_result == 'checkmated'):
        return []
    
    board = chess.Board(fen)

    if not board.is_checkmate():
        return []
    
    if player_color == 'White':
        if player_result == 'win':
            winning_color = chess.WHITE
            checkmated_color = chess.BLACK
        else:
            winning_color = chess.BLACK
            checkmated_color = chess.WHITE
    else:
        if player_result == 'win':
            winning_color = chess.BLACK
            checkmated_color = chess.WHITE
        else:
            winning_color = chess.WHITE
            checkmated_color = chess.BLACK

    # Get position of Checkmated King 
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.KING and piece.color == checkmated_color:
            king_square = square
            break

    # Get possible moves by king
    official_king_moves = board.attacks(king_square)
    attacked_squares = [king_square]
    for square in official_king_moves:
        piece = board.piece_at(square)
    
        if not piece or piece.color != checkmated_color:
            attacked_squares.append(square)

    # Get attacking pieces
    attacking_pieces = []
    for square in attacked_squares:
        attacker_ids = list(board.attackers(color=winning_color, square=square))
        attacking_pieces.extend(attacker_ids)
    attacking_pieces = set(attacking_pieces) # dedup the board pieces based on position

    return sorted([chess.piece_name(board.piece_at(attacker).piece_type) for attacker in attacking_pieces])


@asset(deps=[staging_players_games], group_name='prep')
def player_games(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.sql("SET TimeZone = 'UTC';")
        
        df = conn.sql(f"""
            with player_games as (
                select
                end_time
                , url 
                , pgn
                , time_control
                , rated
                , tcn
                , uuid
                , initial_setup
                , fen
                , time_class
                , rules
                , white__rating
                , white__result
                , white__aid
                , white__username
                , white__uuid
                , black__rating
                , black__result
                , black__aid
                , black__username
                , black__uuid
                , accuracies__white
                , accuracies__black
                from {STAGING_PLAYERS_GAME}
            )
            , final as (
                select
                *
                
                -- Time control details
                , cast(split(time_control, '+')[1] as integer) as time_control_base
                , cast(coalesce(split(time_control, '+')[2], '0') as integer) as time_control_add_seconds
                
                -- PGN details
                , split(pgn, '\n\n')[2] as pgn_moves
                , regexp_extract_all(pgn_moves, '\d+\.+ [\S]+') as pgn_move_extract
                , regexp_extract_all(pgn_moves, '{{\[%clk \S+\]}}') as pgn_clock_extract
                
                -- PGN ECO details
                , regexp_extract(pgn, '(ECO )"(.*)"', 2) as eco
                , regexp_extract(pgn, '(ECOUrl )"(.*)"', 2) as eco_url
                , replace(eco_url, 'https://www.chess.com/openings/', '') as eco_name
                
                -- PLAYER details
                , if(lower(white__username)='{username}', 'White', 'Black') as player_color
                , if(player_color = 'White', white__rating, black__rating) as player_rating
                , if(player_color = 'White', white__result, black__result) as player_result
                
                -- OPPONENT DETAILS
                , if(player_color = 'White', black__rating, white__rating) as opponent_rating
                , if(player_color = 'White', black__result, white__result) as opponent_result
                
                -- PLAYER-OPPONENT DETAILS
                , opponent_rating > player_rating as is_stronger_opponent
                , case 
                    when player_result = 'win' then 'win'
                    when opponent_result = 'win' then 'lose'
                    when player_result <> 'win' and opponent_result <> 'win' then 'draw'
                    else 'unknown'
                end as player_wdl
                , if(player_result='win', opponent_result, player_result) as player_wdl_reason
                
                from player_games
            )
            select * from final
        """).to_df()

        df['checkmate_pieces'] = df[['fen', 'player_color', 'player_result', 'opponent_result']].apply(lambda x: get_checkmate_pieces(x.fen, x.player_color, x.player_result, x.opponent_result), axis=1)
        
        conn.sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_PREP};")
        conn.sql(f"""
            CREATE OR REPLACE TABLE {PREP_PLAYER_GAMES} as (
                select * from df
            );
        """)

    conn.close()