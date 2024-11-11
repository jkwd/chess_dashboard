select
uuid
from {{ ref('prep_player_games_checkmate') }}
where (
    player_result = 'checkmated'
    or opponent_result = 'checkmated'
)
and len(checkmate_pieces) = 0