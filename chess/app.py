import pandas as pd
import duckdb
from chess_pipeline import run_pipeline
import streamlit as st
import altair as alt

from app_helper import load_data, get_daily_win_loss

db = duckdb.connect(":memory:")
db.sql("SET TimeZone='UTC'")
st.set_page_config(layout="wide")

def side():
    st.sidebar.title('Welcome to Chess Dashboard!')
    # username = st.sidebar.text_input("Player username", "magnuscarlsen")
    username = st.sidebar.text_input("Player username", "johnnywhoopp")
    st.sidebar.button('Submit', on_click=click_button, args= [username])

def row1(total_games, total_game_time, win_perc):
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
    
    c2 = (alt.Chart(df)
          .mark_bar()
          .encode(
              x='date',
              y='perc',
              color=alt.Color('result', scale=alt.Scale(domain=domain, range=color_range))
              .legend(orient="bottom")
              )
          )

    st.header("Daily win/draw/lose results")
    col1, col2 = st.columns(2)
    
    col1.altair_chart(c1, use_container_width=True)
    col2.altair_chart(c2, use_container_width=True)

def click_button(username):
    st.title(f'Chess Dashboard for {username}')
    
    run_pipeline(db, username=username)
    df = load_data(db, username)
    
    # Row 1
    total_games= len(df)
    num_win_games = len(df[df['player_result'] == 'win'])
    win_perc = round(100 * num_win_games / total_games, 2)
    total_game_time = str(df['time_played'].sum())

    row1(total_games, total_game_time, win_perc)
    
    # Row 2
    df_daily_win_draw_lose = get_daily_win_loss(db, df)
    row2(df_daily_win_draw_lose)

side()
    

