from chess_etl.assets.core.games import get_checkmate_pieces


def test_get_checkmate_pieces_1():
    fen = '8/8/4R2p/3P2pk/8/5r1K/3r4/8 w - -'
    player_color = 'Black'
    player_result = 'win'
    opponent_result = 'checkmated'
    
    expected_result = ['king', 'pawn', 'rook', 'rook']
    
    assert get_checkmate_pieces(fen=fen, 
                                player_color=player_color, 
                                player_result=player_result, 
                                opponent_result=opponent_result) == expected_result