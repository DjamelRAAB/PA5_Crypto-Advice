import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import cryptocompare

BASE_URL = 'https://min-api.cryptocompare.com/data'

def data_to_dataframe(data):
    """ Transform JSON paylod into Pandas dataframe
    """
    #data from json is in array of dictionaries
    df = pd.DataFrame.from_dict(data)
    
    # time is stored as an epoch, we need normal dates
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)

    return df

def plot_data(df, cryptocurrency, target_currency):
    # got his warning because combining matplotlib 
    # and time in pandas converted from epoch to normal date
    # To register the converters:
    # 	>>> from pandas.plotting import register_matplotlib_converters
    # 	>>> register_matplotlib_converters()
    #  warnings.warn(msg, FutureWarning)
    
    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()
    
    plt.figure(figsize=(15,5))
    plt.cla()
    plt.gcf().canvas.set_window_title('Plot Cryptocurrency')
    plt.title('{} / {} price data'.format(cryptocurrency, target_currency))
    plt.plot(df.index, df.close)
    plt.legend()
    plt.show()
    
    return None

def get_crypto_infos(path_target):
    """ Download the information coin list via Cryptocompare API 
        then transform JSON paylod into Pandas dataframe and save
        in parquet format.
    """
    #data from json is one dictionarie by coin {{coin:{infos}},...}
    coins_infos =  cryptocompare.get_coin_list()

    # Transpose the dataframe to have coin symbol in index and information in columns
    df_coins_infos = pd.DataFrame.from_dict(coins_infos).T

    df_coins_infos.to_parquet(path_target,
                            partition_cols = 'Symbol',
                            compression='snappy')  


if __name__ == "__main__" : 

    # Test save crypto informations in local file system
    get_crypto_infos('./coins-infos.parquet') 
