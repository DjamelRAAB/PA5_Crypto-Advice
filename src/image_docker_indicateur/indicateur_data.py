import json
import requests
from pyspark.sql import *
from pyspark.sql.types import *
import pyspark.sql.functions as F
import datetime
from google.cloud import pubsub_v1

# data from https://api.glassnode.com 
# all asset : ['BTC', 'ETH', 'LTC', 'CREAM', 'CRV', 'PICKLE', 'SUSHI', 'UNI', 'AAVE', 'YAM', 'MX', 'GNO', 'RSR', 'PNK', 'CHSB', 'UMA', 'STAKE', 'YFI', 'MCB', 'FTT', 'BZRX', 'PNT', 'OCEAN', 'MTA', 'BAL', 'BAND', 'AMPL', 'DMG', 'MKR', 'BAT', 'CRO', 'OMG', 'LINK', 'HOT', 'ZRX', 'NPXS', 'HPT', 'HT', 'ENJ', 'KCS', 'SAI', 'WTC', 'SNT', 'MCO', 'WAX', 'ELF', 'PPT', 'MANA', 'DENT', 'SAN', 'RLC', 'LOOM', 'LRC', 'ABT', 'QASH', 'POWR', 'NEXO', 'BNT', 'KNC', 'GUSD', 'EURS', 'FUN', 'POLY', 'BRD', 'STORJ', 'ENG', 'LBA', 'LAMB', 'BIX', 'VERI', 'PAY', 'CVC', 'QKC', 'MFT', 'DGTX', 'TEL', 'AGI', 'DRGN', 'CND', 'QNT', 'ANT', 'CELR', 'UTK', 'MTL', 'TOP', 'WaBi', 'REN', 'MATIC', 'USDT', 'FET', 'DGX', 'PAX', 'SNX', 'USDC', 'LEO', 'WBTC', 'WETH', 'DAI', 'BUSD', 'USDK', 'sUSD', 'REP', 'HUSD', 'OKB', 'NMR', 'UBT', 'RDN', 'COMP', 'wNMX', 'LDO', 'ROOK', 'MIR', 'HEGIC', 'BADGER', 'NFTX', 'PERP', 'RPL', 'DODO', 'BOND', 'DOUGH', 'MLN', 'INDEX', 'CVP', 'ARMOR', 'DHT', 'Nsure', 'NDX', 'DDX']
# insert API key 

import os
project_id = os.environ['project_id']
topic_id = os.environ['topic_id']
API_KEY = os.environ['API_KEY']

def get_all_coin_assets():
    response = requests.get('https://api.glassnode.com/v1/metrics/assets', params={'api_key': API_KEY})
    list = data_to_dataframe(response.json())['symbol']
    return list.to_list()


def get_data_by_coin(spark ,coin, lien , asset_data, date=""):
    # docs : https://docs.glassnode.com/api/transactions
    if date == "" :
         response = requests.get('https://api.glassnode.com/v1/metrics/'+lien+'/' + asset_data,
                            params={'a': coin, 'i': '24h', 'api_key': API_KEY})
    else :
         response = requests.get('https://api.glassnode.com/v1/metrics/'+lien+'/' + asset_data,
                            params={'a': coin, 'i': '24h', 's': date,  'api_key': API_KEY})


    if response.ok :
        return spark.read.json(spark.sparkContext.parallelize([response.json()])).withColumnRenamed('t','time').withColumnRenamed('v',lien+"_"+asset_data).withColumn("coin",F.lit(coin))

    else :
        print(response.text)
        return spark.createDataFrame([coin], 'string').toDF('coin').withColumn("time",F.lit(""))


def get_all_data_by_coin (spark,list_all_asset,coin,date_to_collect=False):

    count = 0
    date = None
    exec("df_result= spark.createDataFrame([coin], 'string').toDF('coin')")
    if date_to_collect :
        yesterday = datetime.date.today() - datetime.timedelta(1)
        date = str(int(yesterday.strftime("%s")) + 80000)
        print(date)

    for (lien, dict) in list_all_asset:
        for (df, asset) in dict :

            if date_to_collect == False :
                exec(df+" = get_data_by_coin(spark, coin, lien, asset)")
            else :
                exec(df+" = get_data_by_coin(spark, coin, lien, asset,"+date+")")
            print(df,date)
            exec (df+".show()")
            if count == 0 :
                exec("df_result = df_result.join("+df+",on=['coin'],how='inner')")
            else :
                exec("df_result = df_result.join("+df+",on=['coin','time'],how='left')")
            count+=1
    list_df = []
    exec("list_df.append(df_result)")
    if date_to_collect :
        return list_df[0].toJSON().collect()[0]
    else : 
        return list_df[0]
   

if __name__ == '__main__':

    spark = SparkSession.builder.master("local")\
            .appName("data_getter").getOrCreate()


    list_price = ["price_usd_ohlc"]
    list_asset_address = ["active_count",  "new_non_zero_count", "count",
                          "receiving_count", "sending_count"]
    list_asset_transactions = ["transfers_volume_sum"]
    list_asset_distribution = ["balance_exchanges_relative","balance_exchanges"]
    list_asset_mining = ["hash_rate_mean","difficulty_latest"]
    dict_asset_market = [("df_"+elt , elt) for elt in list_price]
    dict_asset_address = [("df_"+elt , elt) for elt in list_asset_address]
    dict_asset_transactions = [("df_"+elt , elt) for elt in list_asset_transactions]
    dict_asset_distribution = [("df_"+elt , elt) for elt in list_asset_distribution]
    dict_asset_mining = [("df_"+elt , elt) for elt in list_asset_mining]
    list_all_asset = [('addresses', dict_asset_address), ('transactions', dict_asset_transactions), ('mining', dict_asset_mining)]


    result = get_all_data_by_coin (spark,list_all_asset,"BTC",True)
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic_path, result.encode(), spam='eggs')
    print(future.result())

