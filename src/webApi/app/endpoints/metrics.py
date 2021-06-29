import json
from pydantic import BaseModel
from typing import List, Optional

class CoinMetrics(BaseModel): 
    date : int
    high : float
    low : float
    open : float
    volumefrom : float
    volumeto : float
    close : float
    addresses_active_count : float
    addresses_new_non_zero_count : float
    addresses_count : float
    addresses_receiving_count : float
    addresses_sending_count : float
    transactions_transfers_volume_sum : float
    mining_hash_rate_mean : float
    mining_difficulty_latest : float
    sentiment_analysis : float

class OutCoinMetrics(BaseModel): 
    coin : str
    data : List[CoinMetrics] = []


class TweetMetrics(BaseModel): 
    date: Optional[int] = None
    UrlTweet : Optional[str] = None
    NbComments : Optional[str] = None
    NbLikes : Optional[str] = None
    NbRetweets : Optional[str] = None
    sentiment_analysis : Optional[float] = None
    
class OutTweetMetrics(BaseModel): 
    coin : str
    data : List[TweetMetrics] = []
    

def get_coin_metrics(bqclient, bqstorageclient,  coin : str = 'BTC') :
    # Download query results.
    query_string = f"""
    WITH tweets AS (
    SELECT time, coin, avg(sentiment_analysis) as sentiment_analysis
    FROM `pa5-crypto-advice2.pa5_dataset.coin_tweets`
    GROUP BY time, coin
    )
    SELECT DISTINCT  tweets.time as date ,
        tweets.coin ,
        price.high ,
        price.low ,
        price.open ,
        price.volumefrom ,
        price.volumeto ,
        price.close ,
        metrics.addresses_active_count ,
        metrics.addresses_new_non_zero_count ,
        metrics.addresses_count ,
        metrics.addresses_receiving_count ,
        metrics.addresses_sending_count ,
        metrics.transactions_transfers_volume_sum ,
        metrics.mining_hash_rate_mean ,
        metrics.mining_difficulty_latest ,
        tweets.sentiment_analysis
    FROM `pa5-crypto-advice2.pa5_dataset.coin_glassnode_metrics` as metrics
    JOIN tweets
    ON metrics.time = tweets.time 
    AND metrics.coin = tweets.coin
    JOIN `pa5-crypto-advice2.pa5_dataset.coin_prices` as price
    ON metrics.time = price.time 
    AND metrics.coin = price.coin
    WHERE tweets.coin = '{coin}' 
    ORDER BY date DESC
    LIMIT 10;
    """
    dataframe = (
        bqclient.query(query_string)
        .result()
        .to_dataframe(bqstorage_client=bqstorageclient)
    )
    return {"coin" : coin, "data" : json.loads(dataframe.to_json(orient = 'records'))}  

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

