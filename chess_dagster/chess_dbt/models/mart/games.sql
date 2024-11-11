with game_moves_pivot as (
    PIVOT {{ ref('prep_game_moves') }}
    ON color_move
    USING sum(move_time_seconds) as total_move_time, count(1) as num_moves
    group by uuid
)
, player_games as (
    select *
    from {{ ref('prep_player_games_checkmate') }}
)
, joined as (
    select
    pg.*
    , white_total_move_time
    , white_num_moves
    , black_total_move_time
    , black_num_moves
    from player_games as pg

    left join game_moves_pivot as gm
    on pg.uuid = gm.uuid
)
, final as (
    select
    *

    -- PLAYER DETAILS
    , if(player_color = 'White', white_total_move_time, black_total_move_time) as player_total_move_time
    , if(player_color = 'White', white_num_moves, black_num_moves) as player_num_moves

    -- OPPONENT DETAILS
    , if(player_color = 'White', black_total_move_time, white_total_move_time) as opponent_total_move_time
    , if(player_color = 'White', black_num_moves, white_num_moves) as opponent_num_moves

    from joined
)
select
-- ID
uuid

-- GAME
, url
, rated
, rules
, time_class

-- TIME
, time_control
, time_control_base
, time_control_add_seconds
, time_played_seconds
, game_start_date
, game_start_time
, game_start_timestamp
, game_end_timestamp

-- WHITE-BLACK
, white__uuid
, white__username
, white__aid
, white__rating
, white__result
, white_total_move_time
, white_num_moves

, black__uuid
, black__username
, black__aid
, black__rating
, black__result
, black_total_move_time
, black_num_moves

-- PLAYER-OPPONENT
, player_color
, player_rating
, player_result
, player_total_move_time
, player_num_moves
, opponent_rating
, opponent_result
, opponent_total_move_time
, opponent_num_moves
, is_stronger_opponent
, player_wdl
, player_wdl_reason

-- BOARD
, initial_setup
, fen
, pgn
, pgn_moves
, pgn_move_extract
, pgn_clock_extract
, eco
, eco_url
, eco_name
, checkmate_pieces

-- MISC
, tcn
, accuracies__white
, accuracies__black

from final
