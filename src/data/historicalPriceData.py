import pandas as pd
import requests
from datetime import datetime
from usefuls import BASE_URL, data_to_dataframe, plot_data, save_dataframe_localy
import cryptocompare
from autherData import get_crypto_infos
from os import mkdir, path

# To delete because cryptocompare.get_historical_price* do the samme job 
def get_histo_data(from_sym='BTC', to_sym='USD', timeframe = 'day', limit=2000, aggregation=1, exchange='', toTs=None):
    """ Download the historical data via Cryptocompare API
        using request package 
    """

    url = BASE_URL + '/v2/histo'
    url += timeframe

    last_timestamp = int(datetime.now().timestamp())
    
    parameters = {'fsym': from_sym,
                  'tsym': to_sym,
                  'limit': limit,
                  'aggregate': aggregation,
                  'toTs' : last_timestamp}
    if exchange:
        print('exchange: ', exchange)
        parameters['e'] = exchange    
    
    print('url: ', url) 
    print('timeframe: ', timeframe)
    print('parameters: ', parameters)
    
    # response comes as json
    response = requests.get(url, params=parameters)   

    data = response.json()['Data']['Data'] 
    
    return data

def get_all_histo_data_per_hour (currencies : str, start_date : datetime, target_path: str):
    """ Download the historical data foreach cryptocurrency
        between start_date and now by hour step
    """

    if not path.isdir(target_path) :
        mkdir(target_path)

    cryptocurrency_list = get_crypto_infos().Symbol.tolist()
    timestamp = datetime.now()

    for cryptocurrency in cryptocurrency_list : 
        if not path.isdir(target_path) :
            mkdir(target_path + f'/coin={cryptocurrency}')
        for currency in currencies :  
            try : 
                data = cryptocompare.get_historical_price_hour(cryptocurrency, currency, limit=2000, toTs=timestamp)
                if data is None : raise ValueError
            except : 
                break   
            else : 
                timestamp = datetime.fromtimestamp(data[0]['time'])
                df = pd.DataFrame.from_records(data[1:])
                df['currency'] = currency
                save_dataframe_localy(df, target_path + f'/coin={cryptocurrency}', partition_cols='currency')
                if timestamp < start_date : 
                    break

if __name__ == "__main__" : 
    # cryptocurrency = 'BTC'
    # target_currency = 'USD'

    # # Test get_hist_data 
    # #data = get_histo_data(cryptocurrency, target_currency, 'minute', 1000)
    # data = cryptocompare.get_historical_price_minute('BTC', 'EUR', limit=24, exchange='CCCAGG', toTs=datetime.now())
    # df = data_to_dataframe(data)
    # df.to_parquet('df-minutes.parquet.gzip',
    #           compression='gzip')  # Save data in local file system
    # df = pd.read_parquet('df.parquet.gzip')
    # print(df.tail())
    # plot_data(df, cryptocurrency, target_currency)    


    currencies = ['USD','EUR']
    start_date = datetime(2021,1,1)
    target_path = 'histo-data.parquet'
    get_all_histo_data_per_hour (currencies, start_date, target_path)
