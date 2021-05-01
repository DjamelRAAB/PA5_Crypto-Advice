import pandas as pd
import cryptocompare
from usefuls import save_dataframe_localy

def get_crypto_infos():
    """ Download the coin list informations via Cryptocompare API 
        then transform JSON paylod into Pandas dataframe and save
        it in parquet format.
    """
    #data from json is one dictionarie by coin {{coin:{infos}},...}
    coins_infos =  cryptocompare.get_coin_list()

    # Dataframe that have coin symbol in index and information in columns
    df_coins_infos = pd.DataFrame.from_dict(coins_infos, orient='index')

    # Convert each columns to the right type
    df_coins_infos = df_coins_infos.convert_dtypes()

    return df_coins_infos

    
def get_exchanges_infos():
    """ Download the exchanges informations via Cryptocompare API 
        then transform JSON paylod into Pandas dataframe and save
        it in parquet format.
    """
    #data from json is one dictionarie by exchange {{exchange:{infos}},...}
    exchanges_infos =  cryptocompare.get_exchanges()

    # Dataframe that have exchange Name in index and information in columns
    df_exchanges_infos = pd.DataFrame.from_dict(exchanges_infos, orient='index')
    
    # Convert each columns to the right type
    df_exchanges_infos = df_exchanges_infos.convert_dtypes()
    df_exchanges_infos = df_exchanges_infos.astype({'GradePointsSplit':'string'})

    return df_exchanges_infos


def get_paires_infos():
    """ Download the pairs informations via Cryptocompare API 
        then transform JSON paylod into Pandas dataframe and save
        it in parquet format.
    """
    #data from json is one dictionarie by coin {{coin:{infos}},...}
    pairs_infos = []
    for val in cryptocompare.get_pairs().values():
        pairs_infos.extend(val)
    
    # Transpose the dataframe to have coin symbol in index and information in columns
    df_pairs_infos = pd.DataFrame.from_records(pairs_infos)
    
    # Convert each columns to the right type
    df_pairs_infos = df_pairs_infos.convert_dtypes()

    return df_pairs_infos


if __name__ == "__main__" : 

    # Test save crypto informations in local file system
    save_dataframe_localy(get_crypto_infos(), './coins-infos.parquet', 'Symbol')

    # Test save exchanges informations in local file system
    save_dataframe_localy(get_exchanges_infos(), './exchanges-infos.parquet', 'Name')

    # Test save exchanges informations in local file system
    save_dataframe_localy(get_paires_infos(), './pairs-infos.parquet', 'exchange')
