import dash
import flask
import pandas as pd
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

from apputil.dash import *


# run this with `python app.py` in directory
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    title="simple dash app",
    server=server,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True)

app.layout = html.Div(children=[
    html.Div(children='''
        This is an amazing app
        ''',
        id='heading',
        style={
            'text-align': 'center', 'color': 'gray'
        }),

    html.Div(children=[
        dcc.Dropdown(
            id='num-rows',
            options=[1, 2, 3, 4, 5],
            value=5
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
                    'width': '400px'
                }
        )],
        style={
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "padding-top": "20px",
            "width": "100%"
        })
    ])

@app.callback(
    [Output("summary-table", "columns"),
     Output("summary-table", "data")],
    [Input('num-rows', 'value')])
def num_rows_to_show(nrows):

    df = pd.DataFrame({'my_column': [f'value #{i + 1}' for i in range(5)]})

    cols = [{"name": i, "id": i} for i in df.columns]
    data = df.iloc[:nrows].to_dict('records')

    return cols, data

if __name__ == '__main__':
    # cloud
    app.run_server(host='0.0.0.0', debug=True)

    # debugging
    # app.run_server(host='0.0.0.0', debug=True, port=8050)
