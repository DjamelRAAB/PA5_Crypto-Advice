import json
from pydantic import BaseModel
from typing import List, Optional

class OutCoinMetrics(BaseModel): 
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


class OutSub(BaseModel): 
    date: Optional[int] = None
    UrlTweet : Optional[str] = None
    NbComments : Optional[str] = None
    NbLikes : Optional[str] = None
    NbRetweets : Optional[str] = None
    sentiment_analysis : Optional[float] = None
    
class OutTweetMetrics(BaseModel): 
    coin : str
    data : List[OutSub] = []
    

def get_coin_metrics(coin : str, currency : str, bqclient, bqstorageclient) :
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

def get_tweets_metrics(bqclient, bqstorageclient, coin : str = 'BTC') :
    # Download query results.
    query_string = f"""
    SELECT time as date, UrlTweet, NbComments, NbLikes, NbRetweets, sentiment_analysis
    FROM `pa5-crypto-advice2.pa5_dataset.coin_tweets`
    WHERE coin = '{coin}'
    AND sentiment_analysis != 0.0
    ORDER BY time DESC
    LIMIT 2000;
    """
    dataframe = (
        bqclient.query(query_string)
        .result()
        .to_dataframe(bqstorage_client=bqstorageclient)
    )
    return {"coin" : coin, "data" : json.loads(dataframe.to_json(orient = 'records'))}  

