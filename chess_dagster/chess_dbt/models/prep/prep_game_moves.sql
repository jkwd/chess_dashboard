with player_games as (
    select
    uuid
    , time_class
    , time_control_base
    , time_control_add_seconds
    , pgn_move_extract
    , pgn_clock_extract
    from {{ref('prep_player_games')}}
)
, unnest as (
    select
    *
    , generate_subscripts(pgn_move_extract, 1) AS game_move_index
    , unnest(pgn_move_extract) as move_unnest
    , unnest(pgn_clock_extract) as clock_unnest
    , split(move_unnest, ' ')[1] as color_move_index_raw
    , cast(regexp_replace(color_move_index_raw, '\.+', '') as int) as color_move_index
    , if(regexp_matches(color_move_index_raw, '\.\.\.'), 'Black', 'White') as color_move
    , split(move_unnest, ' ')[2] as move

    -- This is the clock after the addition of time
    , epoch(cast(replace(split(clock_unnest, ' ')[2], ']}}', '') as interval)) as clock_interval_post_move

    -- To get the clock before the addition of time
    , clock_interval_post_move - time_control_add_seconds as clock_interval_move

    from player_games
)
, calculate_time as (
    select
    uuid
    , time_class
    , time_control_base
    , time_control_add_seconds
    , game_move_index
    , color_move
    , color_move_index
    , move
    , coalesce(
        lag(clock_interval_post_move) over(partition by uuid, color_move order by color_move_index)
    , time_control_base
    )  as prev_clock_interval
    , clock_interval_move
    , clock_interval_post_move
    , prev_clock_interval - clock_interval_move as move_time_seconds
    from unnest
)
, final as (
    select
    uuid
    , time_class
    , time_control_base
    , time_control_add_seconds
    , game_move_index
    , color_move
    , color_move_index
    , move
    , if(time_class = 'daily', 0, prev_clock_interval) as prev_clock_interval
    , if(time_class = 'daily', 0, clock_interval_move) as clock_interval_move
    , if(time_class = 'daily', 0, clock_interval_post_move) as clock_interval_post_move
    , if(time_class = 'daily', 0, move_time_seconds) as move_time_seconds
    from calculate_time
)
select
concat(uuid::string, '_', game_move_index::string) as id
, time_class
, time_control_base
, time_control_add_seconds
, uuid::string as uuid
, game_move_index::int as game_move_index
, color_move::string as color_move
, color_move_index::int as color_move_index
, move::string as move
, prev_clock_interval::double as prev_clock_interval
, clock_interval_move::double as clock_interval_move
, clock_interval_post_move::double as clock_interval_post_move
, move_time_seconds::double as move_time_seconds
from final