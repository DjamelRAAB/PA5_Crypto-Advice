# coding: utf-8
from global_variables import SIDEBAR_STYLE
from typing import Sized
import dash_html_components as html
import dash_core_components as dcc
from google.cloud import bigquery
import pandas
import requests
import json
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output


def get_tweets(coin):
    client = bigquery.Client()
    QUERY = (
        f"SELECT UrlTweet,sentiment_analysis FROM `pa5-crypto-advice2.pa5_dataset.coin_tweets` where coin='{coin}' LIMIT 20"
    )  
    query_job = client.query(QUERY).result().to_dataframe()
    return query_job



SIDEBAR_STYLE_TWEETS = {
    "left": 25,
    "bottom": 0,
    "padding": "0rem 3rem",
    "background-color": "#ffffff",
    "overflowY": "scroll",
    "width": "75%",
    'mergin' : 40
    
}

SIDEBAR_STYLE_FRAME={
  "width": "500px",
  "height": "400px",

}

def get_iframs(data):
    result = []
    li = [html.Iframe(id=f"juju{i}",src=f"https://twitframe.com/show?url={data.iloc[i][0]}",style=SIDEBAR_STYLE_FRAME) for i in range(len(data))]
    for key, val in enumerate(li) : 
        result.append(val)
        result.append(
            dbc.Tooltip(f"Sentiments Analysis, {data.iloc[key][1]}", target=f"juju{key}", placement='right')
            )
    return result

def build_page():
    @app.callback(
        Output('tweets', 'children'),
        Input('currency-dropdown', 'value'))
    def update_Iframe (cryptocurrency):
        data=get_tweets(cryptocurrency)
        result  = get_iframs(data)
        return result
                
    children = [
        html.Div(children = dcc.Dropdown(
                    id='currency-dropdown',
                    options=[{'label': "Etherium" , 'value': "ETH"},{'label': "Bitcoin" , 'value': "BTC"} ],
                    value="ETH"),style={
                        "left": 25,
                        "bottom": 0,
                        "padding": "0rem 3rem",
                        "background-color": "#ffffff",
                        "width": "75%",
                        'mergin' : 40

                    }),
        html.Br(),
        html.Br(),
        html.Div(id = 'tweets', children = [], style=SIDEBAR_STYLE_TWEETS)
        ]
    return  html.Div(children)

