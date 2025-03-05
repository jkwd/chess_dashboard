import streamlit as st
import pandas as pd
import duckdb
import os
from datetime import timedelta
import altair as alt

st.set_page_config(layout="wide")

# Connect to the database
conn = duckdb.connect(database=os.getenv("CHESS_DB"), 
                             read_only=True)

# Title of the dashboard
st.title(f"Chess Dashboard for {os.getenv('CHESS_USERNAME')}!")

# Filters
st.subheader('Filters')

filter_1, filter_2 = st.columns(2)
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

ts_min, ts_max = conn.sql(f"""
    select min(game_start_date), max(game_start_date)
    from main.games
    WHERE time_class = '{time_class}'
    AND player_color in ({', '.join([f"'{color}'" for color in player_color])}) 
""").df().iloc[0]
ts_min = pd.Timestamp(ts_min).date()
ts_max = pd.Timestamp(ts_max).date()

st.write(f"Data available from {ts_min} to {ts_max}")

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
move_num = st.slider('1st N moves', min_value=1, max_value=8, value=5)

row_4a, row_4b = st.columns(2)
with row_4a:
    df_starting_moves = conn.sql(f"""
        SELECT
        player_color
        , list_reduce(pgn_move_extract[1: {move_num}],  (s, x) -> s || ' ' || x) as starting_moves
        , count(1) as num_games
        , row_number() over (partition by player_color order by count(1) desc) as rn
        FROM df
        group by player_color, starting_moves
        qualify rn <= 5
        order by player_color, num_games desc
    """).df()
    st.bar_chart(data=df_starting_moves, x='starting_moves', y='num_games', color='player_color', stack=False)

with row_4b:
    df_starting_moves_perc = conn.sql(f"""
        SELECT
        player_color
        , list_reduce(pgn_move_extract[1: {move_num}],  (s, x) -> s || ' ' || x) as starting_moves
        , player_wdl
        , count(1) as num_games
        , 100.0 * count(1) / sum(count(1)) over(partition by player_color, starting_moves) as win_perc
        FROM df
        where starting_moves in (select starting_moves from df_starting_moves)
        group by player_color, starting_moves, player_wdl
    """).df()
    
    bar = alt.Chart(df_starting_moves_perc).mark_bar().encode(
        column="player_color",
        x="starting_moves",
        y="win_perc",
        color="player_wdl",
    )
    st.altair_chart(bar)
    
    
    