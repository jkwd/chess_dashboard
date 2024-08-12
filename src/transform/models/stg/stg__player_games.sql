select *
from {{ source('chess_source', 'player_games') }}