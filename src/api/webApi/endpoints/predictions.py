import json
from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional

class OutPredictPrice(BaseModel): 
    date : str
    coin : str 
    price : int
    currrency : str = 'USD'


class OutPredictSentiment(BaseModel): 
    coin: str
    date : str
    sentiment_24h : Optional[float] = None
    number_tweets_24h : Optional[int] = None


def prediction_price(bqclient, bqstorageclient, coin : str = 'BTC') :
    # Download query results.
    query_string = f"""
    SELECT time as date, coin , price  
    FROM `pa5-crypto-advice2.pa5_dataset.coin_prices_predicted`
    WHERE coin = '{coin}'
    ORDER BY time DESC
    LIMIT 1
    """
    dataframe = (
        bqclient.query(query_string)
        .result()
        .to_dataframe(bqstorage_client=bqstorageclient)
    )
    return json.loads(dataframe.to_json(orient = 'records'))[0]

def prediction_sentiment(bqclient, bqstorageclient, coin : str = 'BTC') :
    # Download query results.
    # today = today = date.today()
    # time = datetime(today.year,today.month,today.day).strftime('%Y-%m-%d %H:%M:%S UTC')
    query_string = f"""
    SELECT time as date , avg(sentiment_analysis) as  sentiment_24h, count(*) as number_tweets_24h
    FROM `pa5-crypto-advice2.pa5_dataset.coin_tweets`
    WHERE coin = '{coin}'
    AND sentiment_analysis != 0.0
    GROUP BY coin, time
    ORDER BY time DESC
    LIMIT 1;
    """
    dataframe = (
        bqclient.query(query_string)
        .result()
        .to_dataframe(bqstorage_client=bqstorageclient)
    )
    data = json.loads(dataframe.to_json(orient = 'records'))
    result = data[0] if len(data)>0 else {}
    result['coin'] =coin 
    return result  

