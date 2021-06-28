import json
from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional

class OutPredictPrice(BaseModel): 
    IdName: Optional[str] = None
    UserName : Optional[str] = None
    time : Optional[str] = None
    Text : Optional[str] = None
    Embtext : Optional[str] = None
    Emojis : Optional[str] = None
    NbComments :Optional[int] = None
    NbLikes :Optional[int] = None 
    NbRetweets : Optional[int] = None
    LinkImage : Optional[str] = None
    UrlTweet : Optional[str] = None
    sentiment_analysis : Optional[float] = None
    coin :str


class OutPredictSentiment(BaseModel): 
    coin: str
    date : str
    sentiment_24h : Optional[float] = None
    number_tweets_24h : Optional[int] = None


def prediction_price(coin : str, currency : str, bqclient, bqstorageclient) :
    # Download query results.
    query_string = """
    SELECT * 
    FROM `pa5-crypto-advice.pa5_dataset.coin_tweets` 
    LIMIT 10
    """
    dataframe = (
        bqclient.query(query_string)
        .result()
        .to_dataframe(bqstorage_client=bqstorageclient)
    )
    return json.loads(dataframe.to_json(orient = 'records'))[0]

def prediction_sentiment(bqclient, bqstorageclient, coin : str = 'BTC') :
    # Download query results.
    today = today = date.today()
    time = datetime(today.year,today.month,today.day).strftime('%Y-%m-%d %H:%M:%S UTC')
    query_string = f"""
    SELECT avg(sentiment_analysis) as  sentiment_24h, count(*) as number_tweets_24h
    FROM `pa5-crypto-advice2.pa5_dataset.coin_tweets`
    WHERE coin = '{coin}'
    AND time = '{time}'
    AND sentiment_analysis != 0.0
    GROUP BY coin, time;
    """
    dataframe = (
        bqclient.query(query_string)
        .result()
        .to_dataframe(bqstorage_client=bqstorageclient)
    )
    data = json.loads(dataframe.to_json(orient = 'records'))
    result = data[0] if len(data)>0 else {}
    result['coin'] =coin 
    result['date'] = time
    return result  

