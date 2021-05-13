import json
import requests
import pandas as pd
from usefuls import *

# data from https://api.glassnode.com 
# all asset : ['BTC', 'ETH', 'LTC', 'CREAM', 'CRV', 'PICKLE', 'SUSHI', 'UNI', 'AAVE', 'YAM', 'MX', 'GNO', 'RSR', 'PNK', 'CHSB', 'UMA', 'STAKE', 'YFI', 'MCB', 'FTT', 'BZRX', 'PNT', 'OCEAN', 'MTA', 'BAL', 'BAND', 'AMPL', 'DMG', 'MKR', 'BAT', 'CRO', 'OMG', 'LINK', 'HOT', 'ZRX', 'NPXS', 'HPT', 'HT', 'ENJ', 'KCS', 'SAI', 'WTC', 'SNT', 'MCO', 'WAX', 'ELF', 'PPT', 'MANA', 'DENT', 'SAN', 'RLC', 'LOOM', 'LRC', 'ABT', 'QASH', 'POWR', 'NEXO', 'BNT', 'KNC', 'GUSD', 'EURS', 'FUN', 'POLY', 'BRD', 'STORJ', 'ENG', 'LBA', 'LAMB', 'BIX', 'VERI', 'PAY', 'CVC', 'QKC', 'MFT', 'DGTX', 'TEL', 'AGI', 'DRGN', 'CND', 'QNT', 'ANT', 'CELR', 'UTK', 'MTL', 'TOP', 'WaBi', 'REN', 'MATIC', 'USDT', 'FET', 'DGX', 'PAX', 'SNX', 'USDC', 'LEO', 'WBTC', 'WETH', 'DAI', 'BUSD', 'USDK', 'sUSD', 'REP', 'HUSD', 'OKB', 'NMR', 'UBT', 'RDN', 'COMP', 'wNMX', 'LDO', 'ROOK', 'MIR', 'HEGIC', 'BADGER', 'NFTX', 'PERP', 'RPL', 'DODO', 'BOND', 'DOUGH', 'MLN', 'INDEX', 'CVP', 'ARMOR', 'DHT', 'Nsure', 'NDX', 'DDX']
# insert API key 
API_KEY = '1sDGH1SMX74Z1deZFm32inPjYId'


def get_all_coin_assets():
    response = requests.get('https://api.glassnode.com/v1/metrics/assets', params={'api_key': API_KEY})
    list = data_to_dataframe(response.json())['symbol']
    return list.to_list()


def get_address_data_by_coin(coin, asset_data):
    # docs : https://docs.glassnode.com/api/addresses
    response = requests.get('https://api.glassnode.com/v1/metrics/addresses/' + asset_data,
                            params={'a': coin, 'i': '24h', 'api_key': API_KEY})
    return data_to_dataframe(response.json())


def get_transactions_data_by_coin(coin, asset_data):
    # docs : https://docs.glassnode.com/api/transactions
    response = requests.get('https://api.glassnode.com/v1/metrics/transactions/' + asset_data,
                            params={'a': coin, 'i': '24h', 'api_key': API_KEY})
    return data_to_dataframe(response.json())


def get_transactions_data_by_coin(coin, asset_data):
    # docs : https://docs.glassnode.com/api/transactions
    response = requests.get('https://api.glassnode.com/v1/metrics/transactions/' + asset_data,
                            params={'a': coin, 'i': '24h', 'api_key': API_KEY})
    return data_to_dataframe(response.json())

if __name__ == '__main__':
    list_asset_address = ["min_10k_count", "min_1k_count", "min_100_count", "min_10_count", "min_1_count",
                          "min_point_1_count", "non_zero_count", "new_non_zero_count", "count", "active_count",
                          "receiving_count", "sending_count"]

    all_coin_accepted_for_address_metric = ['BTC', 'ETH', 'LTC', 'CREAM', 'CRV', 'PICKLE', 'SUSHI', 'UNI', 'AAVE',
                                            'YAM', 'MX', 'GNO', 'RSR', 'PNK', 'CHSB', 'UMA', 'STAKE', 'YFI', 'MCB',
                                            'FTT', 'BZRX', 'PNT', 'OCEAN', 'MTA', 'BAL', 'BAND', 'AMPL', 'DMG', 'MKR',
                                            'BAT', 'CRO', 'OMG', 'LINK', 'HOT', 'ZRX', 'NPXS', 'HPT', 'HT', 'ENJ',
                                            'KCS', 'SAI', 'WTC', 'SNT', 'MCO', 'WAX', 'ELF', 'PPT', 'MANA', 'DENT',
                                            'SAN', 'RLC', 'LOOM', 'LRC', 'ABT', 'QASH', 'POWR', 'NEXO', 'BNT', 'KNC',
                                            'GUSD', 'EURS', 'FUN', 'POLY', 'BRD', 'STORJ', 'ENG', 'LBA', 'LAMB', 'BIX',
                                            'VERI', 'PAY', 'CVC', 'QKC', 'MFT', 'DGTX', 'TEL', 'AGI', 'DRGN', 'CND',
                                            'QNT', 'ANT', 'CELR', 'UTK', 'MTL', 'TOP', 'WaBi', 'REN', 'MATIC', 'USDT',
                                            'FET', 'DGX', 'PAX', 'SNX', 'USDC', 'LEO', 'WBTC', 'WETH', 'DAI', 'BUSD',
                                            'USDK', 'sUSD', 'REP', 'HUSD', 'OKB', 'NMR', 'UBT', 'RDN', 'COMP', 'wNMX',
                                            'LDO', 'ROOK', 'MIR', 'HEGIC', 'BADGER', 'NFTX', 'PERP', 'RPL', 'DODO',
                                            'BOND', 'DOUGH', 'MLN', 'INDEX', 'CVP', 'ARMOR', 'DHT', 'Nsure', 'NDX',
                                            'DDX']

    list_asset_transactions = ["transfers_from_exchanges_count", "transfers_to_exchanges_count","transfers_volume_to_exchanges_sum","transfers_volume_from_exchanges_sum"]
    all_coin_accepted_for_transactions_metric = all_coin_accepted_for_address_metric


    list_asset_transactions = ["balance_exchanges_relative", "balance_exchanges_all","balance_exchanges"]
    all_coin_accepted_for_transactions_metric = all_coin_accepted_for_address_metric


    for asset in list_asset_transactions:
        print(get_transactions_data_by_coin("BTC", asset))





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
