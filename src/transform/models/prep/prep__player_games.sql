with player_games as (
    select
    end_time
    , url 
    , pgn
    , time_control
    , rated
    , tcn
    , uuid
    , initial_setup
    , fen
    , time_class
    , rules
    , white__rating
    , white__result
    , white__aid
    , white__username
    , white__uuid
    , black__rating
    , black__result
    , black__aid
    , black__username
    , black__uuid
    , accuracies__white
    , accuracies__black
    from {{ ref('stg__player_games') }}
)
select
-- PLAYER DETAILS
if(lower(white__username)='{{ var("username")}}', 'White', 'Black') as player_color
, if(player_color = 'White', white__rating, black__rating) as player_rating
, if(player_color = 'White', white__result, black__result) as player_result

-- OPPONENT DETAILS
, if(player_color = 'White', black__rating, white__rating) as opponent_rating
, if(player_color = 'White', black__result, white__result) as opponent_result

-- PLAYER-OPPONENT DETAILS
, player_rating > opponent_rating as is_weaker_opponent
, case player_result
    -- WIN
    when 'win' then 'win'
    
    -- DRAW
    when 'stalemate' then 'draw'
    when 'agreed' then 'draw'
    when 'repetition' then 'draw'
    when '50move' then 'draw'
    when 'insufficient' then 'draw'
    when 'timevsinsufficient' then 'draw'
    
    -- LOSE
    when 'checkmated' then 'lose'
    when 'timeout' then 'lose'
    when 'resigned' then 'lose'
    when 'abandoned' then 'lose'
    when 'threecheck' then 'lose'
end as player_wdl
, if(player_result='win', opponent_result, player_result) as player_wdl_reason

-- GAME DETAILS
, regexp_extract(pgn, '(ECO )"(.*)"', 2) as eco
, cast(replace(regexp_extract(pgn, '(UTCDate )"(.*)"', 2), '.', '-') as date) as start_date
, regexp_extract(pgn, '(StartTime )"(.*)"', 2) as start_time
, cast(concat(start_date, ' ', start_time) as timestamp) as start_timestamp
, cast(end_time as timestamp) as end_timestamp
, age(end_timestamp, start_timestamp) as time_played
, epoch(time_played) as time_played_seconds
, *
from player_games