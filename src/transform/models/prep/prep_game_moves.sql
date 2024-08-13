with player_games as (
    select
    uuid
    , time_control
    , pgn
    from {{ ref('stg__player_games') }}
)
, base as (
    select
    uuid
    , time_control
    , cast(split(time_control, '+')[1] as integer) as time_control_start
    , cast(coalesce(split(time_control, '+')[2], '0') as integer) as time_control_add
    , pgn
    , split(pgn, '\n\n')[2] as pgn_moves
    , regexp_extract_all(pgn_moves, '\d+\.+ [\S]+ {\[%clk \S+\]}') as moves_extract
    from player_games
)
, unnest as (
    select
    uuid
    , time_control
    , time_control_start
    , time_control_add
    , unnest(moves_extract) as moves_unnest
    , split(moves_unnest, ' ')[1] as move_index_raw
    , cast(regexp_replace(move_index_raw, '\.+', '') as int) as move_index
    , if(regexp_matches(move_index_raw, '\.\.\.'), 'Black', 'White') as color_move
    , split(moves_unnest, ' ')[2] as move
    , cast(replace(split(moves_unnest, ' ')[4], ']}', '') as interval) as clock_interval
    , to_seconds(epoch(clock_interval) + time_control_add) as clock_interval_post_move
    from base
)
, final as (
    select 
    uuid
    , time_control
    , time_control_add
    , time_control_start
    , move_index
    , color_move
    , move
    , clock_interval
    , clock_interval_post_move
    , coalesce(
        lag(clock_interval_post_move) over(partition by uuid, color_move order by move_index)
        , to_seconds(time_control_start)
    )  as prev_clock_interval
    , epoch(prev_clock_interval) - epoch(clock_interval)as move_time
    from unnest
)
select * from final