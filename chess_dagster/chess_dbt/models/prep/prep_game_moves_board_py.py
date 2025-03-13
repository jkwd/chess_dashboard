import chess.pgn
from io import StringIO
import chess
import re
import pandas as pd
import numpy as np
from collections import Counter

def get_forked_pieces(fen, to_square):
    forked_pieces = []

    board = chess.Board(fen)
    piece = board.piece_at(to_square)
    piece_color = piece.color
    
    piece_attack_squares = board.attacks(to_square)
    for square in piece_attack_squares:
        attacked_piece = board.piece_at(square)
        if attacked_piece is not None and attacked_piece.color != piece_color and attacked_piece.piece_type != chess.PAWN:
            forked_pieces.append(attacked_piece.symbol())
    
    if len(forked_pieces) < 2:
        return []
    return forked_pieces

def get_captured_piece(prev_fen, fen):
    if prev_fen == "":
        return None
    
    prev_fen = prev_fen.split(' ')[0]
    fen = fen.split(' ')[0]
    prev_pieces = re.findall(r'[prnbqRNBQP]', prev_fen)
    current_pieces = re.findall(r'[prnbqRNBQP]', fen)
    
    prev = Counter(prev_pieces)
    curr = Counter(current_pieces)

    # find the difference between the two lists
    diff = prev-curr
    
    captured = list(diff.elements())
    if len(captured) == 0:
        return None
    
    return captured[0]
    

def model(dbt, session):
    df = dbt.ref("prep_game_moves_fen").to_df()

    # Get board details
    df['prev_fen'] = df.groupby(['game_uuid'])['fen'].shift(1).fillna("")
    df['captured_piece'] = df[['prev_fen', 'fen']].apply(lambda x: get_captured_piece(x['prev_fen'], x['fen']), axis=1)

    # df['move_from_to'] = df['pgn_cum_move'].apply(lambda x: chess.pgn.read_game(StringIO(x)).game().end().move)
    # df['from_square'] = df['move_from_to'].apply(lambda x: x.from_square)
    # df['to_square'] = df['move_from_to'].apply(lambda x: x.to_square)
    # df['moved_piece'] = df[['fen', 'to_square']].apply(lambda x: chess.Board(x['fen']).piece_at(x['to_square']).symbol(), axis=1)
    # df['forked_pieces'] = df[['fen', 'to_square']].apply(lambda x: get_forked_pieces(x['fen'], x['to_square']), axis=1)

    df = df[['id',
            'captured_piece']]
    
    return df