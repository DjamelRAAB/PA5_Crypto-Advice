# google-cloud-bigquery
from google.cloud import bigquery
import pandas
import requests
import json

def get_price_from_bigquery():
    client = bigquery.Client()
    QUERY = (
        'SELECT * FROM `pa5-crypto-advice2.pa5_dataset.coin_prices` '
    )  
    query_job = client.query(QUERY).result().to_dataframe()
    return query_job

def get_predicted_price():
    client = bigquery.Client()
    QUERY = (
        'SELECT * FROM `pa5-crypto-advice2.pa5_dataset.coin_prices_predicted` '
    )  
    query_job = client.query(QUERY).result().to_dataframe()
    return query_job


def get_glassnode_metrics():
    client = bigquery.Client()
    QUERY = (
        'SELECT * FROM `pa5-crypto-advice2.pa5_dataset.coin_glassnode_metrics` '
    )  
    query_job = client.query(QUERY).result().to_dataframe()
    return query_job

def get_tweets():
    client = bigquery.Client()
    QUERY = (
        'SELECT * FROM `pa5-crypto-advice2.pa5_dataset.coin_tweets` '
    )  
    query_job = client.query(QUERY).result().to_dataframe()
    return query_job


def get_actule_price(coin):
    result = requests.get('https://data.messari.io/api/v1/assets/'+coin+'/metrics')
    return result.json()["data"]["market_data"]["price_usd"]


if __name__ == "__main__":
    print(get_actule_price("eth"))
