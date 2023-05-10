import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import yfinance as yf
import pandas as pd
from datetime import date
import plotly
from plotly import graph_objs as go
from tickers import ticker_list

app = dash.Dash()

year_list = ['All']

app.layout = html.Div([
    html.Div(children=[
        html.H1('Stock Monitoring Dashboard', id='header'),
        html.Hr(),
        html.Label('Select Stock Symbol:', className='text'),
        html.Label('', className='whitespace'),
        html.Label('Select Year:', className='text'),
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
        dcc.Dropdown(id='year-dropdown',
        options=[
            {
                'label': str(year_list[i]),
                'value': str(year_list[i]),
            }
            for i in range(len(year_list))
        ],
        value='All',
        searchable=False),
        html.Button(
            'PLOT', 
            id='plot-btn',
            n_clicks=1
            )
    ],
    id='container'),
    dcc.Graph(id='historical-stock-price-graph', animate=True),
])

@app.callback(
    Output('year-dropdown', 'options'),
    [Input('stock-symbol-dropdown', 'value')]
)
def update_dropdown(stock_symbol):
    year_list = ['All']
    stock_ticker = "%s.NS"%stock_symbol
    df = yf.download(stock_ticker)
    
    for year in list(df.index.year.unique()):
        year_list.append(year)

    options = [
            {
                'label': str(year_list[i]),
                'value': str(year_list[i]),
            }
            for i in range(len(year_list))
        ]

    return options
    

@app.callback(
        Output('historical-stock-price-graph', 'figure'),
    [
        Input('plot-btn', 'n_clicks')
    ],
    [
        State('stock-symbol-dropdown', 'value'), 
        State('year-dropdown', 'value')
    ]
) 
def graph_update(n_clicks, stock_symbol, year):
    if n_clicks >= 1:
        stock_ticker = "%s.NS"%stock_symbol
        df = yf.download(stock_ticker)
        
        if year == 'All':
            df_filtered = df
        else:
            df_filtered = df.loc[date(int(year), 1, 1):date(int(year), 12, 31)]
        
        data = [
            go.Scatter(
                x=df_filtered.index,
                y=df_filtered['Open'],
                name='Open',
                mode='lines',
            ),
            go.Scatter(
                x=df_filtered.index,
                y=df_filtered['Close'],
                name='Close',
                mode='lines',
            )
        ]

        
        max_val_y = 0
        min_val_y = 0
        
        if max(df_filtered['Open']) > max(df_filtered['Close']):
            max_val_y = max(df_filtered['Open'])
        else:
            max_val_y = max(df_filtered['Close'])

        fig = {
            'data': data,
            'layout': go.Layout(
                xaxis=dict(range=[min(df_filtered.index), max(df_filtered.index)]), 
                yaxis=dict(range=[min_val_y, max_val_y]),
                xaxis_title='PERIOD',
                yaxis_title='STOCK PRICE (INR)',
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