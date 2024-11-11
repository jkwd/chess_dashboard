with player_games as (
    select
        game_uuid
        , time_class
        , time_control_base
        , time_control_add_seconds
        , pgn_move_extract
        , pgn_clock_extract
    from {{ ref('prep_player_games') }}
)

, unnest as (
    select
        *
        , unnest(pgn_move_extract) as move_unnest
        , split(move_unnest, ' ')[1] as color_move_index_raw
        , cast(regexp_replace(color_move_index_raw, '\.+', '') as int)
            as color_move_index
        , generate_subscripts(pgn_move_extract, 1) as game_move_index
        , unnest(pgn_clock_extract) as clock_unnest
        , if(regexp_matches(color_move_index_raw, '\.\.\.'), 'Black', 'White')
            as color_move
        , split(move_unnest, ' ')[2] as game_move

        -- This is the clock after the addition of time
        , epoch(
            cast(replace(split(clock_unnest, ' ')[2], ']}}', '') as interval)
        ) as clock_interval_post_move

        -- To get the clock before the addition of time
        , clock_interval_post_move
        - time_control_add_seconds as clock_interval_move

    from player_games
)

, calculate_time as (
    select
        game_uuid
        , time_class
        , time_control_base
        , time_control_add_seconds
        , game_move_index
        , color_move
        , color_move_index
        , game_move
        , clock_interval_move
        , clock_interval_post_move
        , coalesce(
            lag(clock_interval_post_move)
                over (
                    partition by game_uuid, color_move order by color_move_index
                )
            , time_control_base
        ) as prev_clock_interval
        , prev_clock_interval - clock_interval_move as move_time_seconds
    from unnest
)

, final as (
    select
        game_uuid
        , time_class
        , time_control_base
        , time_control_add_seconds
        , game_move_index
        , color_move
        , color_move_index
        , game_move
        , if(time_class = 'daily', 0, prev_clock_interval)
            as prev_clock_interval
        , if(time_class = 'daily', 0, clock_interval_move)
            as clock_interval_move
        , if(time_class = 'daily', 0, clock_interval_post_move)
            as clock_interval_post_move
        , if(time_class = 'daily', 0, move_time_seconds) as move_time_seconds
    from calculate_time
)

select
    time_class
    , time_control_base
    , time_control_add_seconds
    , cast(game_uuid as string) as game_uuid
    , cast(game_move_index as int) as game_move_index
    , cast(color_move as string) as color_move
    , cast(color_move_index as int) as color_move_index
    , cast(game_move as string) as game_move
    , cast(prev_clock_interval as double) as prev_clock_interval
    , cast(clock_interval_move as double) as clock_interval_move
    , cast(clock_interval_post_move as double) as clock_interval_post_move
    , cast(move_time_seconds as double) as move_time_seconds
    , concat(cast(game_uuid as string), '_', cast(game_move_index as string))
        as id
from final
