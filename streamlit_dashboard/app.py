import streamlit as st
import altair as alt

import pandas as pd
import duckdb
import os
from datetime import timedelta
import pytz

import io
import chess
import chess.pgn

st.set_page_config(layout="wide")

# Connect to the database
conn = duckdb.connect(database=os.getenv("CHESS_DB"), 
                             read_only=True)

# Title of the dashboard
st.title(f"Chess Dashboard for {os.getenv('CHESS_USERNAME')}!")

filter_1, filter_2, filter_3 = st.columns(3)
with filter_1: 
    df_time_class = conn.sql("""
        SELECT DISTINCT time_class
        FROM main.games
        order by time_class
    """).df()
    time_class = st.selectbox('Time Class', df_time_class, index=2)
    
with filter_2: 
    filter_player_color = conn.sql("""
        SELECT DISTINCT player_color
        FROM main.games
        order by player_color
    """).df()['player_color'].tolist()
    filter_player_color = ['All'] + filter_player_color
    player_color = st.selectbox('Player Color', filter_player_color)
    player_color = [player_color]
    if player_color == ['All']:
        player_color = ['White', 'Black']

with filter_3:
    timezones = pytz.all_timezones
    utc_index = timezones.index("UTC")
    selected_timezone = st.selectbox("Select a timezone", timezones, index=utc_index)

ts_min, ts_max = conn.sql(f"""
    select min(game_start_date), max(game_start_date)
    from main.games
    WHERE time_class = '{time_class}'
    AND player_color in ({', '.join([f"'{color}'" for color in player_color])}) 
""").df().iloc[0]
ts_min = pd.Timestamp(ts_min).date()
ts_max = pd.Timestamp(ts_max).date()

(slider_min, slider_max) = st.slider(
     "Game Date",
     min_value = ts_min,
     max_value = ts_max,
     value = (ts_min, ts_max),
     format="YYYY-MM-DD")

st.divider()

# Get base data
query = f"""
    SELECT *
    FROM main.games
    WHERE time_class = '{time_class}'
    AND player_color in ({', '.join([f"'{color}'" for color in player_color])})
    AND game_start_date between '{slider_min}' and '{slider_max}'
"""
df = conn.sql(query).df()

# Row 1
row_1a, row_1b, row_1c, row_1d = st.columns(4)

with row_1a:
    st.subheader('# Games')
    st.header(df.shape[0])

with row_1b:
    df_player_wdl = conn.sql("""
        SELECT 
        sum(if(player_wdl = 'win', 1, 0)) / count(1) as win_perc
        FROM df
    """).df()
    
    st.subheader('Win %')
    st.header(f"{df_player_wdl['win_perc'].iloc[0]:.2%}")

with row_1c:
    st.subheader('# Moves Made')
    st.header(df['player_num_moves'].sum())

with row_1d:
    st.subheader('Total Move time')
    if time_class != 'daily':
        move_time = df['player_total_move_time'].sum()
        move_time = timedelta(seconds=move_time)
        move_time = timedelta(days=move_time.days, seconds=move_time.seconds)
        st.header(str(move_time))
    else:
        st.header('NA')

# Row 2
st.subheader('Elo across time')
df_daily_games = conn.sql("""
    with data as (
        SELECT
        game_start_date
        , player_rating
        , game_start_timestamp
        , row_number() over (partition by game_start_date order by game_start_timestamp) as game_num
        FROM df
    )
    select
    game_start_date
    , max_by(player_rating, game_num) as player_rating
    , count(1) as num_games
    from data
    group by game_start_date
""").df()

base = alt.Chart(df_daily_games).encode(x='game_start_date')
line =  base.mark_line(color='red').encode(
    y='player_rating',
    tooltip=['game_start_date', 'player_rating', 'num_games']
)
bar = base.mark_bar().encode(
    y='num_games',
    tooltip=['game_start_date', 'player_rating', 'num_games']
)

st.altair_chart(bar+line, use_container_width=True)

# Row 3
row_3a, row_3b = st.columns(2)

with row_3a:
    st.subheader('Win/Draw/Loss')
    df_wdl = conn.sql("""
        SELECT 
        player_wdl
        , count(1) as num_games
        , 100.0 * count(1) / sum(count(1)) over() as win_perc
        FROM df
        group by player_wdl
    """).df()
    st.bar_chart(data=df_wdl, x='player_wdl', y='win_perc')

with row_3b:
    st.subheader('Win/Draw/Loss with Reason')
    df_wdl_reason = conn.sql("""
        SELECT
        player_wdl
        , player_wdl_reason
        , count(1) as num_games
        , 100.0 * count(1) / sum(count(1)) over() as win_perc
        FROM df
        group by player_wdl, player_wdl_reason
    """).df()
    
    bar = alt.Chart(df_wdl_reason).mark_bar().encode(
        x='player_wdl',
        y=alt.X('sum(win_perc)').stack("normalize"),
        color='player_wdl_reason'
    )
    st.altair_chart(bar, use_container_width=True)
    

# Row 4
row_4a, row_4b = st.columns(2)
df_dow_hour = conn.sql(f"""
    set timezone='{selected_timezone}';
    with base as (
        select
        game_start_timestamp::VARCHAR || ' UTC' as game_start_timestamp_utc
        , game_start_timestamp_utc::TIMESTAMPTZ as ts
        , player_wdl
        from df
    )
    select
        hour(ts) as ts_hour
        , dayofweek(ts) as ts_day_of_week
        , case ts_day_of_week
            when 0 then 'Sunday'
            when 1 then 'Monday'
            when 2 then 'Tuesday'
            when 3 then 'Wednesday'
            when 4 then 'Thursday'
            when 5 then 'Friday'
            when 6 then 'Saturday'
            else 'Unknown'
        end as ts_day_of_week_name
        , *
    from base;
""").df()

with row_4a:
    st.subheader('Games by Day of Week')
    base = alt.Chart(df_dow_hour).encode(
        alt.X('ts_day_of_week_name', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
        y="count()",
    )
    st.altair_chart(base.mark_bar())

with row_4b:
    st.subheader('Win rate by Day of Week')
    base = alt.Chart(df_dow_hour).encode(
        alt.X('ts_day_of_week_name', 
              sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ),
        alt.Y('count()', stack='normalize'),
        color='player_wdl'
    )
    st.altair_chart(base.mark_bar())
    

row_5a, row_5b = st.columns(2)

with row_5a:
    st.subheader('Games by Hour')
    base = alt.Chart(df_dow_hour).encode(
        alt.X('ts_hour', bin={"binned": True, "step": 1}),
        y="count()",
    )
    st.altair_chart(base.mark_bar())

with row_5b:
    st.subheader('Win rate by Hour')
    base = alt.Chart(df_dow_hour).encode(
        alt.X('ts_hour', bin={"binned": True, "step": 1}),
        alt.Y('count()', stack='normalize'),
        color='player_wdl'
    )
    st.altair_chart(base.mark_bar())


st.subheader('Win rate by Day of Week X Hour')
df_heatmap = conn.sql(f"""
    select
    ts_day_of_week_name
    , ts_hour
    , 100.0 * count_if(player_wdl = 'win') / count(1) as perc
    , count(1) as num_games
    from df_dow_hour
    group by ts_day_of_week_name, ts_hour
""").df()

heatmap = alt.Chart(df_heatmap).mark_rect().encode(
    alt.Y('ts_day_of_week_name', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
    alt.X('ts_hour', bin={"binned": True, "step": 1}),
    color='perc',
    tooltip=['ts_day_of_week_name', 'ts_hour', 'perc', 'num_games']
)
st.altair_chart(heatmap, use_container_width=True)


row_6a, row_6b = st.columns(2)
df_checkmate_pieces = conn.sql("""
        select
        player_wdl
        , checkmate_pieces
        , count(1) as num_games
        from df
        where player_wdl_reason = 'checkmated'
        group by all
        order by player_wdl, num_games desc;
    """).df()

with row_6a:
    st.subheader('Winning checkmate Pieces')
    df_checkmate_pieces_win = df_checkmate_pieces[df_checkmate_pieces['player_wdl'] == 'win']
    st.dataframe(df_checkmate_pieces_win, hide_index=True)

with row_6b:
    st.subheader('Losing checkmate Pieces')
    df_checkmate_pieces_lose = df_checkmate_pieces[df_checkmate_pieces['player_wdl'] == 'lose']
    st.dataframe(df_checkmate_pieces_lose, hide_index=True)


# Row 7/8
move_num = st.slider('1st N moves', min_value=1, max_value=7, value=5)
st.header(f'Most played starting {move_num} moves')

df_starting_moves = conn.sql(f"""
    with cte as (
        SELECT
        player_color
        , player_wdl
        , list_reduce(pgn_move_extract[1:{move_num}], (s, x) -> s || ' ' || x) as starting_moves
        , count(1) as wdl_num_games
        , sum(count(1)) over(partition by player_color, starting_moves) as num_games
        FROM df
        group by player_color, player_wdl, starting_moves
    )
    select
        *
        , dense_rank() over(partition by player_color order by num_games desc) as rn
        , 100.0 * wdl_num_games / num_games as perc
    from cte
    qualify rn <= 5
""").df()

if 'White' in player_color:
    df_winning_opening_white = conn.sql(f"""
            select
            *
            , row_number() over(order by perc desc) as win_order
            from df_starting_moves
            where player_color = 'White'
            and player_wdl = 'win'
            qualify win_order <= 3
        """).df()
    
    df_losing_opening_white = conn.sql(f"""
            select
            *
            , row_number() over(order by perc desc) as lose_order
            from df_starting_moves
            where player_color = 'White'
            and player_wdl = 'lose'
            qualify lose_order <= 3
        """).df()
    
    st.subheader('Top 3 Best/Worst opening moves: White')
    total_white = len(df_winning_opening_white) + len(df_losing_opening_white)
    for i, col in enumerate(st.columns(total_white)):
        if i < len(df_winning_opening_white):
            with col:
                opening = df_winning_opening_white['starting_moves'].iloc[i]
                perc = df_winning_opening_white['perc'].iloc[i].round(2)
                
                pgn = io.StringIO(opening)
                game = chess.pgn.read_game(pgn)
                board = game.end().board()
                
                st.write(f'Win {perc}%')
                st.write(chess.svg.board(board), unsafe_allow_html=True)
                if st.toggle('List Games', key=f'White_{i}'):
                    df_display = conn.sql(f"""
                        select *
                        from (
                            select
                            game_analysis_url
                            from df
                            where player_color = 'White'
                            and player_wdl = 'win'
                            and list_reduce(pgn_move_extract[1:{move_num}], (s, x) -> s || ' ' || x) = '{opening}'
                        )
                        using sample 5 rows;
                    """).df()

                    st.dataframe(df_display, 
                                 column_config={
                                     'game_analysis_url': st.column_config.LinkColumn(
                                        "URL", display_text="Game URL")
                                     }
                                 )
                    
                
        else:
            with col:
                opening = df_losing_opening_white['starting_moves'].iloc[len(df_winning_opening_white)-i]
                perc = df_losing_opening_white['perc'].iloc[len(df_winning_opening_white)-i].round(2)
                
                pgn = io.StringIO(opening)
                game = chess.pgn.read_game(pgn)
                board = game.end().board()
                
                st.write(f'Lose {perc}%')
                st.write(chess.svg.board(board), unsafe_allow_html=True)
                if st.toggle('List Games', key=f'White_{i}'):
                    df_display = conn.sql(f"""
                        select *
                        from (
                            select
                            game_analysis_url
                            from df
                            where player_color = 'White'
                            and player_wdl = 'lose'
                            and list_reduce(pgn_move_extract[1:{move_num}], (s, x) -> s || ' ' || x) = '{opening}'
                        )
                        using sample 5 rows;
                    """).df()

                    st.dataframe(df_display, 
                                 column_config={
                                     'game_analysis_url': st.column_config.LinkColumn(
                                        "URL", display_text="Game URL")
                                     }
                                 )
    

if 'Black' in player_color:
    df_winning_opening_black = conn.sql(f"""
            select
            *
            , row_number() over(order by perc desc) as win_order
            from df_starting_moves
            where player_color = 'Black'
            and player_wdl = 'win'
            qualify win_order <= 3
        """).df()
    
    df_losing_opening_black = conn.sql(f"""
            select
            *
            , row_number() over(order by perc desc) as lose_order
            from df_starting_moves
            where player_color = 'Black'
            and player_wdl = 'lose'
            qualify lose_order <= 3
        """).df()
    
    st.subheader('Top 3 Best/Worst opening moves: Black')
    total_black = len(df_winning_opening_black) + len(df_losing_opening_black)
    for i, col in enumerate(st.columns(total_black)):
        if i < len(df_winning_opening_black):
            with col:
                opening = df_winning_opening_black['starting_moves'].iloc[i]
                perc = df_winning_opening_black['perc'].iloc[i].round(2)
                
                pgn = io.StringIO(opening)
                game = chess.pgn.read_game(pgn)
                board = game.end().board()
                
                st.write(f'Win {perc}%')
                st.write(chess.svg.board(board, orientation=chess.BLACK), unsafe_allow_html=True)
                if st.toggle('List Games', key=f'Black_{i}'):
                    df_display = conn.sql(f"""
                        select *
                        from (
                            select
                            game_analysis_url
                            from df
                            where player_color = 'Black'
                            and player_wdl = 'win'
                            and list_reduce(pgn_move_extract[1:{move_num}], (s, x) -> s || ' ' || x) = '{opening}'
                        )
                        using sample 5 rows;
                    """).df()

                    st.dataframe(df_display, 
                                 column_config={
                                     'game_analysis_url': st.column_config.LinkColumn(
                                        "URL", display_text="Game URL")
                                     }
                                 )
        else:
            with col:
                opening = df_losing_opening_black['starting_moves'].iloc[len(df_winning_opening_black)-i]
                perc = df_losing_opening_black['perc'].iloc[len(df_winning_opening_black)-i].round(2) 
                
                pgn = io.StringIO(opening)
                game = chess.pgn.read_game(pgn)
                board = game.end().board()
                
                st.write(f'Lose {perc}%')
                st.write(chess.svg.board(board, orientation=chess.BLACK), unsafe_allow_html=True)
                if st.toggle('List Games', key=f'Black_{i}'):
                    df_display = conn.sql(f"""
                        select *
                        from (
                            select
                            game_analysis_url
                            from df
                            where player_color = 'Black'
                            and player_wdl = 'lose'
                            and list_reduce(pgn_move_extract[1:{move_num}], (s, x) -> s || ' ' || x) = '{opening}'
                        )
                        using sample 5 rows;
                    """).df()

                    st.dataframe(df_display, 
                                 column_config={
                                     'game_analysis_url': st.column_config.LinkColumn(
                                        "URL", display_text="Game URL")
                                     }
                                 )

# Close connection
conn.close()                