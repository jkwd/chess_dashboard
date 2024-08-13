import duckdb
import streamlit as st
import altair as alt
from datetime import datetime

from load.load_chess_data import run_pipeline
from src.streamlit.app_helper import prep_player_games, create_game_moves_table, get_game_moves, get_daily_win_loss, wdl_by_color

from dbt.cli.main import dbtRunner, dbtRunnerResult

db = duckdb.connect("chess.duckdb")
db.sql("SET TimeZone='UTC'")
st.set_page_config(layout="wide")

domain = ['win', 'draw', 'lose']
color_range = ['#2669c9', 'grey', '#f9abab']

def row1(df):
    total_games= len(df)
    num_win_games = len(df[df['player_result'] == 'win'])
    win_perc = round(100 * num_win_games / total_games, 2)
    total_game_time = str(df['time_played'].sum())
    highest_rating = df['player_rating'].max()
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.subheader('# Games Played')
    col1.subheader(total_games)
    
    col2.subheader('Total Game Time')
    col2.subheader(total_game_time)
    
    col3.subheader('Overall Win %')
    col3.subheader(f'{win_perc}%')
    
    col4.subheader('Highest Rating')
    col4.subheader(highest_rating)

def row2(df):   
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

    st.header("Daily Win/Draw/Loss results")
    
    st.altair_chart(c1, use_container_width=True)

def row3(df):
    col1, col2 = st.columns(2)
    
    bar1 = (alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X('sum(num_games)'),
                y='player_color'
            )
    )
    
    text1 = (alt.Chart(df)
            .mark_text(dx=-15, dy=3, color='black')
            .encode(
                x=alt.X('sum(num_games)'),
                y='player_color',
                text=alt.Text('sum(num_games)')
            )
    )
    
    bar2 = (alt.Chart(df)
          .mark_bar()
          .encode(
                x=alt.X('sum(perc)').stack("normalize"),
                # x='perc',
                y='player_color',
                color=alt.Color('result', scale=alt.Scale(domain=domain, range=color_range))
                .legend(orient="bottom")
            )
    )
    text2 = (alt.Chart(df)
            .mark_text(dx=-15, dy=3, color='white')
            .encode(
                x=alt.X('sum(perc)').stack("normalize"),
                # x='perc',
                y='player_color',
                detail='result',
                text=alt.Text('perc', format='.1f')
            )
    )
    
    
    col1.subheader('# Games Played by color')
    col1.altair_chart(bar1+text1, use_container_width=True)
    
    col2.subheader('% Win/Draw/Loss by color')
    col2.altair_chart(bar2+text2, use_container_width=True)

def run():
    st.sidebar.title('Welcome to Chess Dashboard!')
    username = st.sidebar.text_input("Player username", placeholder="magnuscarlsen")
    
    if username and ('username' not in st.session_state or username != st.session_state.username):
        if 'username' not in st.session_state or username != st.session_state.username:
            st.session_state.username = username
        run_pipeline(db, username=username)
        
        print(db.sql("select * from information_schema.tables"))
        print(db.sql("select * from chess_data_raw.player_games ").to_df().info())
        
        df = prep_player_games(db, username)
        st.session_state.df = df # Save to session for filters
        
        create_game_moves_table(db, df)
        df_game_moves = get_game_moves(db)
        st.session_state.df_game_moves = df_game_moves # Save to session for filters
        
        # initialize
        dbt = dbtRunner()

        # create CLI args as a list of strings
        cli_args = ["run", "--project-dir", "src/transform", "--profiles-dir", "src/transform/profiles", "--vars", f"{{'username': {username}}}"]

        # run the command
        res: dbtRunnerResult = dbt.invoke(cli_args)

        # inspect the results
        for r in res.result:
            print(f"{r.node.name}: {r.status}")
        
        print(db.sql("select * from information_schema.tables"))
    if 'df' in st.session_state:
        df = st.session_state.df
        df_game_moves = st.session_state.df_game_moves
        
        filter_start_date = df['start_date'].min().to_pydatetime()
        filter_end_date = df['start_date'].max().to_pydatetime()
        
        start_date = st.sidebar.date_input(
            "Filter Start Date",
            filter_start_date,
            filter_start_date,
            filter_end_date,
            format="YYYY-MM-DD"
        )
        
        end_date = st.sidebar.date_input(
            "Filter End Date",
            filter_end_date,
            filter_start_date,
            filter_end_date,
            format="YYYY-MM-DD"
        )
        
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())
        df_filtered = df[(df['start_date'] >= start_date) & (df['start_date'] <= end_date)]
        
        # Row 1 - Big numbers
        row1(df_filtered)

        # Row 2 - Daily win lose draw
        df_daily_win_draw_lose = get_daily_win_loss(db, df_filtered)
        row2(df_daily_win_draw_lose)

        # Row 3 - Win by color
        df_color_wdl = wdl_by_color(db, df_filtered)
        row3(df_color_wdl)

if __name__ == "__main__":
    run()