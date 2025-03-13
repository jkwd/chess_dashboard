import chess.pgn
from io import StringIO
import chess

def model(dbt, session):
    df = dbt.ref("prep_game_moves").to_df()

    # Get board details
    df['fen'] = df[['pgn_header' , 'pgn_cum_move']].apply(lambda x: chess.pgn.read_game(StringIO(x['pgn_header'] + '\n\n' + x['pgn_cum_move'])).game().end().board().fen(), axis=1)
    
    df = df[[
        'id',
        'game_uuid',
        'game_move_index',
        'fen',
    ]]
    
    return df