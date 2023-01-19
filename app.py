import os

import dash
import flask
import pandas as pd
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
from apputil.dash import conditional_formatting
from apputil.data import add_fake_user, last_row_to_dash


# run this with `python app.py` in directory
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    title="simple dash app",
    server=server,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True)

# Connect to database
engine = create_engine(os.environ['RAILWAY_SQL_URL'])

app.layout = html.Div(children=[
    html.Div(children='''
        Choose the number of random coffee reviews to view.
        ''',
        id='heading',
        style={
            'text-align': 'center', 
            'color': 'gray'
        }),

    html.Div(children=[
        dcc.Dropdown(
            id='num-rows',
            options=[i for i in range(10)],
            value=3
        )],
        style={
            'text-align': 'center',
            'width': "50%",
            'padding-left': '25%'
        }),

    html.Div([dash_table.DataTable(
            id='summary-table',
            fixed_columns={'headers': True},
            page_action='none',
            style_as_list_view=True,
            style_cell={
                    'textAlign': 'center',
                    'whiteSpace': 'normal',
                    'width': '400px',
                    'height': 'auto',
                    'padding': '5px'
                },
            style_table={
                    'height': '500px',
                    'overflowX': 'auto',
                    'overflowY': 'auto'
                    },
            style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'max-width': '250px'
                    },
            style_data_conditional=conditional_formatting(
                [('stars', '# < 3', 'white', 'red')]
            )
        )],
        style={
            "width": "60%",
            "display": "block",
            "float": "center",
            "margin": "auto",
            "padding-top": "20px",
        }),

    html.Div([], id='last-row'),

    dcc.Loading(
        id="loading-update-button",
        children=[
            html.Div([
                html.Button(
                    'Update Data', 
                    id='update-button',
                    n_clicks=0),
            ],
                style={
                    'text-align': 'center'
                })],
        type="circle",
    ),

    dcc.Store(id='stored-last-row')
    ])

@app.callback(
    [Output("summary-table", "columns"),
     Output("summary-table", "data"),
     Output("last-row", "children")],
    [Input('num-rows', 'value'),
     Input('stored-last-row', 'data')])
def num_rows_to_show(nrows, stored_last_row):
    df = pd.read_sql('coffee', engine)
    df_ = df.sample(nrows)
    cols = [{"name": i, "id": i} for i in df_.columns]
    data = df_.to_dict('records')
    
    last_row = last_row_to_dash(df)

    return cols, data, last_row

@app.callback(
    [Output("update-button", "n_clicks"),
     Output('stored-last-row', 'data')],
    [Input('update-button', 'n_clicks')])
def update_data_button(nclicks):
    if nclicks == 1:
        df_new = add_fake_user(engine)
        return 0, df_new.to_dict()
    else:
        return 0, None
    

if __name__ == '__main__':
    # cloud
    # app.run_server(host='0.0.0.0', debug=True)

    # debugging
    app.run_server(host='0.0.0.0', debug=True, port=8050)
