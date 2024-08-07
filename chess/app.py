import pandas as pd
import duckdb
from chess_pipeline import run_pipeline
import streamlit as st
import altair as alt

from app_helper import load_data, get_daily_win_loss

db = duckdb.connect(":memory:")
db.sql("SET TimeZone='UTC'")
st.set_page_config(layout="wide")

def row1(df):
    total_games= len(df)
    num_win_games = len(df[df['player_result'] == 'win'])
    win_perc = round(100 * num_win_games / total_games, 2)
    total_game_time = str(df['time_played'].sum())
    
    col1, col2, col3 = st.columns(3)
    
    col1.subheader('# Games Played')
    col1.subheader(total_games)
    
    col2.subheader('Total Game Time')
    col2.subheader(total_game_time)
    
    col3.subheader('Overall Win %')
    col3.subheader(f'{win_perc}%')

def row2(df):
    domain = ['win', 'draw', 'lose']
    color_range = ['#2669c9', 'grey', '#f9abab']
    
    c1 = (alt.Chart(df)
          .mark_bar()
          .encode(
              x='date',
              y='num_games',
              color=alt.Color('result', scale=alt.Scale(domain=domain, range=color_range))
              .legend(orient="bottom")
              )
          )
    
    # c2 = (alt.Chart(df)
    #       .mark_bar()
    #       .encode(
    #           x='date',
    #           y='perc',
    #           color=alt.Color('result', scale=alt.Scale(domain=domain, range=color_range))
    #           .legend(orient="bottom")
    #           )
    #       )

    st.header("Daily win/draw/lose results")
    
    st.altair_chart(c1, use_container_width=True)

st.sidebar.title('Welcome to Chess Dashboard!')
prev_username = None
username = st.sidebar.text_input("Player username", placeholder="magnuscarlsen")

if username and ('username' not in st.session_state or username != st.session_state.username):
    if 'username' not in st.session_state or username != st.session_state.username:
        st.session_state.username = username
    run_pipeline(db, username=username)
    df = load_data(db, username)
    
    st.session_state.df = df

if 'df' in st.session_state:
    df = st.session_state.df
    filter_start_date = df['start_date'].min().to_pydatetime()
    filter_end_date = df['start_date'].max().to_pydatetime()
    
    start_date, end_date = st.sidebar.slider(
        'Select a date range',
        value=(filter_start_date, filter_end_date),
        format='YYYY-MM-DD'
    )
    
    df_filtered = df[(df['start_date'] >= start_date) & (df['start_date'] <= end_date)]
    
    # Row 1 - Big numbers
    row1(df_filtered)

    # Row 2 - Daily win lose draw
    df_daily_win_draw_lose = get_daily_win_loss(db, df_filtered)
    row2(df_daily_win_draw_lose)

    # Row 3 - 