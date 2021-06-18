import json
import requests
import pandas as pd
from pyspark.sql import *
from pyspark.sql.types import *
import pyspark.sql.functions as F
import datetime

# data from https://api.glassnode.com 
# all asset : ['BTC', 'ETH', 'LTC', 'CREAM', 'CRV', 'PICKLE', 'SUSHI', 'UNI', 'AAVE', 'YAM', 'MX', 'GNO', 'RSR', 'PNK', 'CHSB', 'UMA', 'STAKE', 'YFI', 'MCB', 'FTT', 'BZRX', 'PNT', 'OCEAN', 'MTA', 'BAL', 'BAND', 'AMPL', 'DMG', 'MKR', 'BAT', 'CRO', 'OMG', 'LINK', 'HOT', 'ZRX', 'NPXS', 'HPT', 'HT', 'ENJ', 'KCS', 'SAI', 'WTC', 'SNT', 'MCO', 'WAX', 'ELF', 'PPT', 'MANA', 'DENT', 'SAN', 'RLC', 'LOOM', 'LRC', 'ABT', 'QASH', 'POWR', 'NEXO', 'BNT', 'KNC', 'GUSD', 'EURS', 'FUN', 'POLY', 'BRD', 'STORJ', 'ENG', 'LBA', 'LAMB', 'BIX', 'VERI', 'PAY', 'CVC', 'QKC', 'MFT', 'DGTX', 'TEL', 'AGI', 'DRGN', 'CND', 'QNT', 'ANT', 'CELR', 'UTK', 'MTL', 'TOP', 'WaBi', 'REN', 'MATIC', 'USDT', 'FET', 'DGX', 'PAX', 'SNX', 'USDC', 'LEO', 'WBTC', 'WETH', 'DAI', 'BUSD', 'USDK', 'sUSD', 'REP', 'HUSD', 'OKB', 'NMR', 'UBT', 'RDN', 'COMP', 'wNMX', 'LDO', 'ROOK', 'MIR', 'HEGIC', 'BADGER', 'NFTX', 'PERP', 'RPL', 'DODO', 'BOND', 'DOUGH', 'MLN', 'INDEX', 'CVP', 'ARMOR', 'DHT', 'Nsure', 'NDX', 'DDX']
# insert API key 
API_KEY = '1sDGH1SMX74Z1deZFm32inPjYId'


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
        if asset_data == "price_usd_ohlc" and coin == "BTC":
            return spark.read.json(spark.sparkContext.parallelize([response.json()])).\
                withColumnRenamed('t','time').\
                    withColumnRenamed('v',lien+"_"+asset_data).\
                        withColumn("coin",F.lit(coin)).\
                            withColumn("open",F.col("o.o")).\
                            withColumn("high",F.col("o.h")).\
                            withColumn("low",F.col("o.l")).\
                            withColumn("close",F.col("o.c")).drop("o")

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

    exec("df_result.orderBy('time').coalesce(1).write.csv('./"+ coin +"',header='true')")


if __name__ == '__main__':

    spark = SparkSession.builder.master("local").appName("data_getter").getOrCreate()

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

    # ca recupere toute les donnée 
    # get_all_data_by_coin (spark,list_all_asset,"BTC")

    get_all_data_by_coin (spark,list_all_asset,"BTC",True)



    # ca recupere que pour la journee
    # get_all_data_by_coin (spark,list_all_asset,"ETH",True)
    # et_all_data_by_coin (spark,list_all_asset,"BTC")

    #get_address_data_by_coin()
    #list_asset_transactions = ["transfers_from_exchanges_count", "transfers_to_exchanges_count","transfers_volume_to_exchanges_sum","transfers_volume_from_exchanges_sum"]
    #all_coin_accepted_for_transactions_metric = all_coin_accepted_for_address_metric
    #list_asset_transactions = ["balance_exchanges_relative", "balance_exchanges_all","balance_exchanges"]
    #all_coin_accepted_for_transactions_metric = all_coin_accepted_for_address_metric
    # def get_transactions_data_by_coin(coin, asset_data):
    #     # docs : https://docs.glassnode.com/api/transactions
    #     response = requests.get('https://api.glassnode.com/v1/metrics/transactions/' + asset_data,
    #                             params={'a': coin, 'i': '24h', c : "USD", 'api_key': API_KEY})
    #     return data_to_dataframe(response.json())
    # res = requests.get('https://api.glassnode.com/v1/metrics/addresses/active_count',
    #      params={'a': 'ETH', 'i':'24h' ,'api_key': API_KEY })
    # convert to pandas dataframe
    # url = "http://open-api.bybt.com/api/pro/v1/futures/liquidation_chart"
    # payload = {}
    # headers = {
    #     'symbol' : "ETH",
    #   'bybtSecret': '79407aeae74d4574afd72054532dad82'
    # }
    # response = requests.request("GET", url, headers=headers, data = payload)
    # print(response.text.encode('utf8'))
