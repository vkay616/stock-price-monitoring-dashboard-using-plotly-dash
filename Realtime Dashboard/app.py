import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from googlefinanceapi import GFA
import pandas as pd
from datetime import date
import plotly
from plotly import graph_objs as go
from tickers import ticker_list

app = dash.Dash()
gfa = GFA()

X = []
Y = []

app.layout = html.Div([
    html.Div(children=[
        html.H1('Stock Monitoring Dashboard', id='header'),
        html.Hr(),
        html.Label('Select Stock Symbol:', className='text'),
        html.Br(),
        dcc.Dropdown(id='stock-symbol-dropdown',
        options=[
            {
                "label": str(ticker_list[i]),
                "value": str(ticker_list[i]),
            }
            for i in range(len(ticker_list))
        ],
        value='RELIANCE',
        searchable=True
        ),
        html.Button(
            'PLOT', 
            id='plot-btn',
            n_clicks=1
            )
    ],
    id='container'),
    dcc.Graph(id='realtime-stock-price-graph', animate=True),
    dcc.Interval(
            id='interval-component',
            interval=5*1000,
            n_intervals=0
        )
])
   

@app.callback(
        Output('realtime-stock-price-graph', 'figure'),
    [
        Input('interval-component', 'n_intervals',)
    ],
) 
def graph_update(interval):

    # stock_tracker = "RELIANCE"
    # if stock_symbol != stock_tracker:
    #         X.clear()
    #         Y.clear()
    #         stock_tracker = stock_symbol

    Y.append(gfa.get('RELIANCE', 'NSE'))
    X.append(len(Y))
    print(X, Y)
     
    data = [
        go.Scatter(
            x=list(X),
            y=list(Y),
            mode='lines',
        ),
    ]

    fig = {
        'data': data,
        'layout': go.Layout(
            xaxis_title='',
            yaxis_title='',
            xaxis=dict(range=[min(X),max(X)]),
            yaxis = dict(range = [min(Y),max(Y)]),
            font=dict(
                family='Helvetica',
                size=18,
                color='cadetblue'
            ),
            )
        }

            
    return fig


if __name__ == '__main__':
    app.run_server()