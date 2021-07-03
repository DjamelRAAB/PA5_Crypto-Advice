# coding: utf-8
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import callback_context
from app import app
from datetime import datetime, timedelta
from flask import request
import json
import global_variables as gv
import dash
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import cryptocompare
import plotly.graph_objects as go
import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage


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
CRYPTOCURRENCY = 'ETH'
CURRENCY = 'USDT'
DURATION = 'day'

# Explicitly create a credentials object. This allows you to use the same
# credentials for both the BigQuery and BigQuery Storage clients, avoiding
# unnecessary API calls to fetch duplicate authentication tokens.
credentials, your_project_id = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Make clients.
BQ_CLIENT = bigquery.Client(credentials=credentials, project=your_project_id,)
BQ_STORAGE_CLIENT = bigquery_storage.BigQueryReadClient(credentials=credentials)

def build_page():
    global CRYPTOCURRENCY, CURRENCY, EXCHANGE, DURATION
    
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

    @app.callback(
        Output('coins-dropdown', 'options'),
        Input('exchange-dropdown', 'value'))
    def set_coin_list(selected_exchnage):
        PAIRS_PATH='./data/pairs-infos.parquet'
        df_pairs = pd.read_parquet(f'{PAIRS_PATH}/exchange={selected_exchnage}',columns=['fsym'])
        fsym = df_pairs.fsym.tolist()
        label_coins = [{'label': symbol , 'value': symbol} for symbol in fsym]
        return label_coins

    @app.callback(
        Output('currency-dropdown', 'options'),
        Input('exchange-dropdown', 'value'),
        Input('coins-dropdown', 'value'))
    def set_currency_list(selected_exchnage, cryptocurrency):
        PAIRS_PATH='./data/pairs-infos.parquet'
        df_pairs = pd.read_parquet(f'{PAIRS_PATH}/exchange={selected_exchnage}',columns=['fsym','tsym'])
        df_pairs = df_pairs[df_pairs.fsym == cryptocurrency]
        tsym = df_pairs.tsym.tolist()
        currencies = [{'label': currency , 'value': currency} for currency in tsym]
        return currencies
    
    @app.callback(
        Output('update-graph-series', 'children'),
        Output('update-graph-candles', 'children'),
        Input('graph-update', 'n_intervals'),
        Input('submit-button-state', 'n_clicks'),
        State('coins-dropdown', 'value'),
        State('currency-dropdown', 'value'),
        State('exchange-dropdown', 'value'),
        State('duration-radioitem', 'value'))
    def update_graphs(n_intervals, n_clicks, cryptocurrency, currency, exchange, duration):
        global BQ_CLIENT, BQ_STORAGE_CLIENT
        
        to_timestamp = datetime.now()
        data = historical_function(duration)(cryptocurrency, currency, exchange=exchange, limit=250, toTs=to_timestamp)
        df_trad_data =  pd.DataFrame.from_records(data)
        df_trad_data.time = df_trad_data.time.apply(lambda row : datetime.fromtimestamp(row))

        fig_candles = go.Figure(data=[go.Candlestick(x=df_trad_data['time'],
            open=df_trad_data['open'], high=df_trad_data['high'],
            low=df_trad_data['low'], close=df_trad_data['close'])
            ])
        fig_candles.update_layout(
            title=f"{cryptocurrency} candles price from {exchange}",
            xaxis_title="Time",
            yaxis_title=f"Price {currency}"
        )
        fig_candles.update_layout(xaxis_rangeslider_visible=True)
        fig_candles.update_xaxes(rangeslider_visible=True)

        fig_series = go.Figure()
        fig_series.add_trace(go.Scatter(x=df_trad_data.time, y=df_trad_data.close, mode='lines',name='Real price'))
        # Download query results.
        if cryptocurrency  in ['BTC','ETH'] and duration == 'day':
            query_string = f"""
            SELECT DISTINCT time, price 
            FROM `pa5-crypto-advice2.pa5_dataset.coin_prices_predicted`
            WHERE coin = '{cryptocurrency}'
            ORDER BY time DESC
            LIMIT 250;
            """
            df_predicted_data = (
                BQ_CLIENT.query(query_string)
                .result()
                .to_dataframe(bqstorage_client=BQ_STORAGE_CLIENT)
            )
            fig_series.add_trace(go.Scatter(x=df_predicted_data.time, y=df_predicted_data.price, mode='lines',name='Predicted price'))  
        
        fig_series.update_layout(
            title=f"{cryptocurrency} price from {exchange}",
            xaxis_title="Time",
            yaxis_title=f"Price {currency}"
        )
        fig_series.update_layout(xaxis_rangeslider_visible=True)
        fig_series.update_xaxes(rangeslider_visible=True)

        return [dcc.Graph( id='graph-series', figure=fig_series )],\
                [dcc.Graph( id='graph-candles', figure=fig_candles)]



    @app.callback(
        Output('update-graph-metrics', 'children'),
        Input('submit-button-state', 'n_clicks'),
        State('coins-dropdown', 'value'))
    def update_metrics( n_clicks, cryptocurrency):
        global BQ_CLIENT, BQ_STORAGE_CLIENT
        # Download query results.
        if cryptocurrency not in ['BTC','ETH']:
            return [] 
        query_string = f"""
        SELECT DISTINCT time, mining_hash_rate_mean as hash_rate
        FROM `pa5-crypto-advice2.pa5_dataset.coin_glassnode_metrics`
        WHERE coin = '{cryptocurrency}'
        ORDER BY time DESC
        LIMIT 250;
        """
        df_trad_data = (
            BQ_CLIENT.query(query_string)
            .result()
            .to_dataframe(bqstorage_client=BQ_STORAGE_CLIENT)
        )
        df_trad_data.time = pd.to_datetime(df_trad_data.time, unit='s')

        fig_metrics = px.line(df_trad_data, x='time', y='hash_rate')
        fig_metrics.update_layout(
            title=f"{cryptocurrency} Hash Rate",
            xaxis_title="Time",
            yaxis_title="Hash rate mean"
        )
        fig_metrics.update_layout(xaxis_rangeslider_visible=True)
        fig_metrics.update_xaxes(rangeslider_visible=True)

        return [
            dcc.Graph(id='graph-metrics',
            figure=fig_metrics)
            ]

    @app.callback(
        Output('update-graph-sentiment', 'children'),
        Input('submit-button-state', 'n_clicks'),
        State('coins-dropdown', 'value'))
    def update_sentiment( n_clicks, cryptocurrency):
        global BQ_CLIENT, BQ_STORAGE_CLIENT
        # Download query results.
        if cryptocurrency not in ['BTC','ETH']:
            return [] 
        query_string = f"""
        SELECT DISTINCT time, avg(sentiment_analysis) as sentiment
        FROM `pa5-crypto-advice2.pa5_dataset.coin_tweets`
        WHERE coin = '{cryptocurrency}'
        AND sentiment_analysis != 0.0
        GROUP BY time
        ORDER BY time DESC
        LIMIT 250;
        """
        df_trad_data = (
            BQ_CLIENT.query(query_string)
            .result()
            .to_dataframe(bqstorage_client=BQ_STORAGE_CLIENT)
        )
        df_trad_data.time = pd.to_datetime(df_trad_data.time, unit='s')
        df_trad_data.sentiment = df_trad_data.sentiment * 100
        df_trad_data.sentiment = df_trad_data.sentiment - 10

        fig_sentiment = px.line(df_trad_data, x='time', y='sentiment')
        fig_sentiment.add_bar(x=df_trad_data.time, y=df_trad_data.sentiment,name='')

        fig_sentiment.update_layout(
            title=f"{cryptocurrency} Sentiment",
            xaxis_title="Time",
            yaxis_title="Price variation %"
        )

        fig_sentiment.update_layout(xaxis_rangeslider_visible=True)
        fig_sentiment.update_xaxes(rangeslider_visible=True)

        return [
            dcc.Graph(id='graph-sentiment',
            figure=fig_sentiment)
            ]
    
    df_exchanges = pd.read_parquet('./data/exchanges-infos.parquet', columns=['InternalName','Name'])
    label_exchanges = [{'label': inname , 'value': name} for name, inname in zip(df_exchanges.InternalName,df_exchanges.Name)]
    del(df_exchanges)

    children=([
        html.Div([
            html.Label('Exchange'),
            dcc.Dropdown(
                id='exchange-dropdown',
                options=label_exchanges,
                value=EXCHANGE,
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

        ]),
        dcc.Interval(id="graph-update", interval=1000*60),

        html.Div(id = 'update-graph-series' , children=[
            dcc.Graph(id='graph-series', animate=True),
        ]),

        html.Div(id='update-graph-sentiment',children=[
            dcc.Graph(id='graph-sentiment', animate=True),
        ]),

        html.Div(id = 'update-graph-candles' , children=[
            dcc.Graph(id='graph-candles', animate=True),
        ]),

        html.Div(id='update-graph-metrics',children=[
            dcc.Graph(id='graph-metrics', animate=True),
        ]),

    ])

    app.layout = html.Div(style={'padding': '20px'}, children=children)

    return app.layout