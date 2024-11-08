import pandas as pd
def model(dbt, session):
    
    upstream_df = dbt.ref("dbt_prep_player_games").to_df()
    
    df = pd.DataFrame({'id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Charlie']})
    
    return df