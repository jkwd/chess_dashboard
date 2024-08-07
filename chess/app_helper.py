def load_data(db, username):
    return db.sql(f"""
        select
        -- PLAYER DETAILS
        if(lower(white__username)='{username}', 'White', 'Black') as player_color
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
        from chess_data.player_games
    """).to_df()

def get_daily_win_loss(db, df):
    return db.sql("""
        select 
        start_date as date
        , player_wdl as result
        , count(1) as num_games
        , sum(num_games) over(partition by start_date) as daily_num_games
        , 100.0 * num_games / daily_num_games as perc
        from df
        group by start_date, player_wdl
    """).to_df()

def wdl_by_color(db, df):
    return db.sql("""
        select
        coalesce(player_color, 'All') as player_color
        , player_wdl as result
        , count(1) as num_games
        , round(100.0 * count(1) / sum(count(1)) over(partition by player_color),2) as perc
        from df
        group by grouping sets(
            (player_color, player_wdl)
            , (player_wdl)
        )
    """).to_df()