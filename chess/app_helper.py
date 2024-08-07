def load_data(db, username):
    df = db.sql(f"""
    select
        if(lower(white__username)='{username}', 'White', 'Black') as player_color
        , if(player_color = 'White', white__result, black__result) as player_result
        , if(player_color = 'White', black__result, white__result) as opponent_result
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
        end as win_draw_lose
        , if(player_result='win', opponent_result, player_result) as reason
        , regexp_extract(pgn, '(ECO )"(.*)"', 2) as eco
        , replace(regexp_extract(pgn, '(UTCDate )"(.*)"', 2), '.', '-') as start_date
        , regexp_extract(pgn, '(StartTime )"(.*)"', 2) as start_time
        , cast(concat(start_date, ' ', start_time) as timestamp) as start_timestamp
        , cast(end_time as timestamp) as end_timestamp
        , age(end_timestamp, start_timestamp) as time_played
        , *
        from chess_data.player_games
""").to_df()
    return df

def get_daily_win_loss(db, df):
    df = db.sql("""
        select 
        start_date as date
        , win_draw_lose as result
        , count(1) as num_games
        , sum(num_games) over(partition by start_date) as daily_num_games
        , 100.0 * num_games / daily_num_games as perc
        from df
        group by start_date, win_draw_lose
    """).to_df()
    return df