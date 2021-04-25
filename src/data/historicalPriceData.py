import pandas as pd
import requests
from datetime import datetime
from utils import BASE_URL, data_to_dataframe, plot_data

def get_hist_data(from_sym='BTC', to_sym='USD', timeframe = 'day', limit=2000, aggregation=1, exchange='', toTs=None):
    """ Download the JSON via Cryptocompare API
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