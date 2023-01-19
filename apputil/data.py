import numpy as np
import pandas as pd
from dash import html


def add_fake_user(engine):
    # get the highest index so far
    max_index = pd.read_sql('SELECT MAX(index) FROM coffee', engine).iloc[0][0]

    # Build a fake user, and their fake row of data
    user_id = f"B{pd.Timestamp.today()}"
    stars = np.random.choice(range(1, 6))
    review = f'Today is {pd.Timestamp.today().date()}, and I think this thing is a solid {stars}.'

    df_new = pd.DataFrame({
        'user_id': [user_id],
        'stars': [stars],
        'reviews': [review],
        'date': [pd.Timestamp.today().date()]
    }, index=[max_index + 1])

    df_new.to_sql('coffee', engine, if_exists='append')

    print("Added new row to the 'coffee' table in the database.")

    return df_new

def last_row_to_dash(df):
    row_ = [
            'Last Review:',
            html.Br(),
            f'index: {df.tail(1).index.values[0]}',
            html.Br(),
            f'user_id: {df.tail(1)["user_id"].values[0]}',
            html.Br(),
            f'reviews: {df.tail(1)["reviews"].values[0]}',
        ]
    
    return row_