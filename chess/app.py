import pandas as pd
import duckdb
from chess_pipeline import run_pipeline
import streamlit as st

from app_helper import load_data

db = duckdb.connect(":memory:")
st.title('Welcome to Chess Dashboard!')

def side():
    username = st.sidebar.text_input("Player username", "magnuscarlsen")
    st.sidebar.button('Submit', on_click=click_button, args= [username])

def top(total_games, win_perc):
    col1, col2, col3 = st.columns(3)
    
    col1.subheader('# Games Played')
    col1.subheader(total_games)
    
    col2.subheader('Overall Win %')
    col2.subheader(f'{win_perc}%')
    
    col3.subheader('# Games Played')

def click_button(username):
    st.subheader(f'Chess Dashboard for {username}')
    
    run_pipeline(db, username=username)
    df = load_data(db, username)
    total_games= len(df)
    num_win_games = len(df[df['player_result'] == 'win'])
    win_perc = round(100 * num_win_games / total_games, 2)

    top(total_games, win_perc)

side()
    

