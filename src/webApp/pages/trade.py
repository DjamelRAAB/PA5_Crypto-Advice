# coding: utf-8
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import callback_context
from app import app
from datetime import datetime
from flask import request
import json
import src.webApp.global_variables as gv
import dash
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import cryptocompare
import plotly.graph_objects as go


def historical_function(duration):
    switcher={
            "minute": cryptocompare.get_historical_price_minute,
            "hour": cryptocompare.get_historical_price_hour,
            "day": cryptocompare.get_historical_price_day,
            }
    return switcher.get(duration, None)


def init_current_data(cryptocurrency, currency, exchange):
        data = cryptocompare.get_price(cryptocurrency, currency=currency, full=True)['DISPLAY'][cryptocurrency]
        df = pd.DataFrame.from_dict(data)
        df['Data'] = df.index
        df = df.drop('IMAGEURL')
        df.reset_index(drop=True, inplace=True)
        df['Value'] = df[currency] 
        del df[currency]
        return df.to_dict('records')
        

def init_historical_data(cryptocurrency, currency, exchange, duration):
        to_timestamp = datetime.now()
        data = historical_function(duration)(cryptocurrency, currency, exchange=exchange, limit=2000, toTs=to_timestamp)
        df_historical_data =  pd.DataFrame.from_records(data)
        df_historical_data.time = df_historical_data.time.apply(lambda row : datetime.fromtimestamp(row))
        return df_historical_data

# Default values 
EXCHANGE = 'Binance'
CRYPTOCURRENCY = 'BTC'
CURRENCY = 'EUR'
DURATION = 'minute'
N_CLICKS = 0 

def build_page():
    global CRYPTOCURRENCY, CURRENCY, EXCHANGE, DURATION, DF_TRAD_DATA
    
    @app.callback(
        Output('coins-dropdown', 'options'),
        Input('exchange-dropdown', 'value'))
    def set_coin_list(selected_exchnage):
        fsym = ["btc","ETH"]
        label_coins = [{'label': symbol , 'value': symbol} for symbol in fsym]
        return label_coins

    @app.callback(
        Output('currency-dropdown', 'options'),
        Input('exchange-dropdown', 'value'),
        Input('coins-dropdown', 'value'))
    def set_currency_list(selected_exchnage, cryptocurrency):
        tsym = ["btc","ETH"]
        currencies = [{'label': currency , 'value': currency} for currency in tsym]
        return currencies
    
    @app.callback(
        Output('graph-candles', 'figure'),
        Output('graph-series', 'figure'),
        Input('graph-update', 'n_intervals'),
        Input('submit-button-state', 'n_clicks'),
        State('coins-dropdown', 'value'),
        State('currency-dropdown', 'value'),
        State('exchange-dropdown', 'value'),
        State('duration-radioitem', 'value'))
    def update_graphs(n_intervals, n_clicks, cryptocurrency, currency, exchange, duration):

        to_timestamp = datetime.now()
        data = historical_function(duration)(cryptocurrency, currency, exchange=exchange, limit=2000, toTs=to_timestamp)
        DF_TRAD_DATA =  pd.DataFrame.from_records(data)
        DF_TRAD_DATA.time = DF_TRAD_DATA.time.apply(lambda row : datetime.fromtimestamp(row))
        
        # else :  
        #     to_timestamp = datetime.now()
        #     data = historical_function(duration)(cryptocurrency, currency, exchange=exchange, limit=1, toTs=to_timestamp)
        #     df = pd.DataFrame.from_records(data[1:])
        #     df.time = df.time.apply(lambda row : datetime.fromtimestamp(row))
        #     DF_TRAD_DATA = DF_TRAD_DATA[1:].append(df)
        
        fig_candles = go.Figure(data=[go.Candlestick(x=DF_TRAD_DATA['time'],
            open=DF_TRAD_DATA['open'], high=DF_TRAD_DATA['high'],
            low=DF_TRAD_DATA['low'], close=DF_TRAD_DATA['close'])
            ])
        fig_candles.update_layout(
            title=f"{cryptocurrency} candles price from {exchange}",
            xaxis_title="Time",
            yaxis_title=f"Price {currency}"
        )
        fig_candles.update_layout(xaxis_rangeslider_visible=True)

        fig_series = px.line(DF_TRAD_DATA, x='time', y='close')
        fig_series.update_layout(
            title=f"{cryptocurrency} price from {exchange}",
            xaxis_title="Time",
            yaxis_title=f"Price {currency}",
            # xaxis=dict(range=[min(DF_TRAD_DATA.time), max(DF_TRAD_DATA.time)]),
            # yaxis=dict(range=[min(DF_TRAD_DATA.close), max(DF_TRAD_DATA.close)])
        )
        fig_series.update_xaxes(rangeslider_visible=True)

        return fig_candles, fig_series    
    
    @app.callback(
        Output('graph-update', 'interval'),
        Input('submit-button-state', 'n_clicks'),
        State('duration-radioitem', 'value'))
    def refresh_interval(n_clicks, duration):
        switcher={
            "minute": 1000*60 ,
            "hour": 1000*60*60,
            "day": 1000*60*60*24
            }
        interval = switcher.get(duration, None)

        return interval
    
    #df_coins = pd.read_parquet('/home/raab/5GES/S2/PA5/PA5_Crypto-Advice/coins-infos.parquet', columns=['FullName','Symbol'])
    df_exchanges = pd.DataFrame(["binance"])

    #label_coins = [{'label': full_name , 'value': symbol} for full_name, symbol in zip(df_coins.FullName,df_coins.Symbol)]
    label_exchanges = [{"binance","bnb"} ]

    #del(df_coins)
    del(df_exchanges)

    children=([
        html.Div([
            html.Label('Exchange'),
            dcc.Dropdown(
                id='exchange-dropdown',
                options=label_exchanges,
                value=EXCHANGE
            ),
            html.Label('Crypto currency'),
            dcc.Dropdown(
                id='coins-dropdown',
                options=[{'label': CRYPTOCURRENCY , 'value': CRYPTOCURRENCY}],
                value=CRYPTOCURRENCY
            ),
            html.Label('Target currency'),
            dcc.Dropdown(
                id='currency-dropdown',
                options=[{'label': CURRENCY , 'value': CURRENCY}],
                value=CURRENCY
            ),
        
            html.Label('Duration'),
            dcc.RadioItems(
                id='duration-radioitem',
                options=[
                    {'label': 'Minute', 'value': 'minute'},
                    {'label': 'Hour', 'value': 'hour'},
                    {'label': 'Day', 'value': 'day'}
                ],
                value=DURATION, 
                labelStyle={'display': 'inline-block'}
            ),
            html.Button(id='submit-button-state', n_clicks=0, children='Submit'),

        ]), # , style={'columnCount': 2}
        html.Div([
            html.Div([
                dcc.Graph(id='graph-series', animate=True),
                dcc.Graph(id='graph-candles', animate=True),
                dcc.Interval(id="graph-update", interval=1000*60)
            ]),
        ])
    ])

    app.layout = html.Div(style={'padding': '20px'}, children=children)

    return app.layout