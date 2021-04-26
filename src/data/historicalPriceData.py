import pandas as pd
import requests
from datetime import datetime
from utils import BASE_URL, data_to_dataframe, plot_data
import cryptocompare

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


if __name__ == "__main__" : 
    cryptocurrency = 'BTC'
    target_currency = 'USD'

    # Test get_hist_data 
    #data = get_histo_data(cryptocurrency, target_currency, 'minute', 1000)
    data = cryptocompare.get_historical_price_minute('BTC', 'EUR', limit=24, exchange='CCCAGG', toTs=datetime.now())
    df = data_to_dataframe(data)
    df.to_parquet('df-minutes.parquet.gzip',
              compression='gzip')  # Save data in local file system
    df = pd.read_parquet('df.parquet.gzip')
    print(df.tail())
    plot_data(df, cryptocurrency, target_currency)    

