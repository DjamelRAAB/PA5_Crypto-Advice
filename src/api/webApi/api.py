import json
import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage
from fastapi import FastAPI
from typing import Optional
from endpoints.predictions import OutPredictPrice, OutPredictSentiment
from endpoints.predictions import prediction_price, prediction_sentiment
from endpoints.metrics import OutTweetMetrics, OutCoinMetrics
from endpoints.metrics import get_coin_metrics, get_tweets_metrics


# Explicitly create a credentials object. This allows you to use the same
# credentials for both the BigQuery and BigQuery Storage clients, avoiding
# unnecessary API calls to fetch duplicate authentication tokens.
credentials, your_project_id = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Make clients.
BQ_CLIENT = bigquery.Client(credentials=credentials, project=your_project_id,)
BQ_STORAGE_CLIENT = bigquery_storage.BigQueryReadClient(credentials=credentials)

BASE_URL = '/cryptoadvice/api/'
app = FastAPI(openapi_url=f"{BASE_URL}openapi.json" , docs_url=f"{BASE_URL}", redoc_url=f"{BASE_URL}redoc")

@app.get(f"/", include_in_schema=False)
async def public():
    return {"status":200}

@app.get(f"{BASE_URL}prediction/price" , response_model = OutPredictPrice)
async def predict_price(coin : str):
    return prediction_price(coin = coin, bqclient= BQ_CLIENT, bqstorageclient= BQ_STORAGE_CLIENT)

@app.get(f"{BASE_URL}prediction/sentiment", response_model = OutPredictSentiment)
async def predict_sentiment(coin : str):
    return prediction_sentiment(coin = coin, bqclient= BQ_CLIENT, bqstorageclient= BQ_STORAGE_CLIENT)

@app.get(f"{BASE_URL}metrics", response_model = OutCoinMetrics)
async def coin_metrics(coin : str):
    return get_coin_metrics (coin= coin, bqclient= BQ_CLIENT, bqstorageclient= BQ_STORAGE_CLIENT)

@app.get(f"{BASE_URL}tweets", response_model = OutTweetMetrics)
async def tweets_metrics(coin : str):
    return get_tweets_metrics(coin= coin, bqclient= BQ_CLIENT, bqstorageclient= BQ_STORAGE_CLIENT)