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
        , CAST(end_time AS DATE) AS date_played_utc
        , date_part('hour', end_time) as hour_played_utc
        , *
        from chess_data.player_games
""").to_df()
    return df