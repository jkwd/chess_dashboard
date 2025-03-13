with player_games as (
    select
    game_uuid
    , time_class
    , time_control_base
    , time_control_add_seconds
    , pgn_header
    , pgn_move_extract
    , pgn_clock_extract
    from {{ ref('prep_player_games') }}
)
, unnest as (
    select
    *

    -- Move details
    , generate_subscripts(pgn_move_extract, 1) as game_move_index
    , unnest(pgn_move_extract) as move_unnest
    , unnest(pgn_clock_extract) as clock_unnest
    , split(move_unnest, ' ')[1] as color_move_index_raw
    , regexp_replace(color_move_index_raw, '\.+', '') as color_move_index_str
    , if(
        regexp_matches(color_move_index_raw, '\.\.\.'), 'Black', 'White'
    ) as color_move
    , split(move_unnest, ' ')[2] as game_move

    -- This is the clock after the addition of time
    , epoch(
        cast(replace(split(clock_unnest, ' ')[2], ']}}', '') as interval)
    ) as clock_interval_post_move

    -- To get the clock before the addition of time
    , clock_interval_post_move - time_control_add_seconds as clock_interval_move

     from player_games
)
select
    -- Game details
    game_uuid || '_' || game_move_index as id
    , game_uuid
    , time_class
    , time_control_base
    , time_control_add_seconds
    
    -- Move details
    , game_move_index
    , pgn_header
    , string_agg(move_unnest, ' ') over(partition by game_uuid order by game_move_index) as pgn_cum_move
    , color_move
    , cast(color_move_index_str as int) as color_move_index
    , game_move
    
    -- Clock details
    , if(time_class = 'daily', 0, clock_interval_move) as clock_interval_move
    , if(time_class = 'daily', 0, clock_interval_post_move) as clock_interval_post_move
    , if(time_class = 'daily', 
        0, 
        coalesce(
            lag(clock_interval_post_move)
                over (
                    partition by game_uuid, color_move order by color_move_index
                )
            , time_control_base
        )
    ) as prev_clock_interval
    , if(time_class = 'daily', 0, prev_clock_interval - clock_interval_move) as move_time_seconds

from unnest