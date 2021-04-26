import requests
from utils import BASE_URL
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cryptocompare
from datetime import datetime 

##### GET CURRENT PRICE DATA USING requests PACKAGE
def get_exchange_cypto_price(cryptocurrency='BTC', currency='USD', exchange=''):
    """ Wrapper route /data/price of cryptocompare API 
        with using crypto currency and target currency and exchange parameters
    """
    url = BASE_URL + '/price'    
    
    # Somme other parameters dont used here is described in cryptocompare API documentation 
    parameters = {'fsym': cryptocurrency,
                  'tsyms': currency }
    
    if exchange:
        print('exchange: ', exchange)
        parameters['e'] = exchange
        
    # response comes as json
    response = requests.get(url, params=parameters)   
    data = response.json()
    try : 
        data = data[currency]
    except KeyError : 
        data = -1

    return data  

##### GET CURRENT PRICE DATA USING cryptocompare PACKAGE
def get_crypto_price(cryptocurrency,currency):
    """ Wrapper route /data/price of cryptocompare API 
        with using crypto currency and target currency parameters
    """
    return cryptocompare.get_price(cryptocurrency,currency=currency)[cryptocurrency][currency]

def get_cryptos_prices(cryptocurrency,currency):
    """ Wrapper route /data/price of cryptocompare API 
        with using list crypto currency and/or list target currency parameters
    """
    return cryptocompare.get_price(cryptocurrency,currency=currency)

def get_crypto_name(cryptocurrency):
    """ Wrapper route /data/all/coinlist of cryptocompare API 
        wich return FullName of crypto currency
    """
    return cryptocompare.get_coin_list()[cryptocurrency]['FullName']

def animate(i, cryptocurrency, currency):
    """ Animation diplay real time plot of one crypto currency in spécifique currency
    """
    x_vals.append(datetime.now())
    y_vals.append(get_crypto_price(cryptocurrency,currency))

    plt.cla()
    plt.title(get_crypto_name(cryptocurrency) + ' Price Live Plotting')
    plt.gcf().canvas.set_window_title('Live Plotting Cryptocurrency')
    
    plt.xlabel('Date')
    plt.ylabel('Price($)')
    plt.plot_date(x_vals,y_vals,linestyle="solid",ms=0)
    plt.tight_layout()

def func_animation(cryptocurrency, currency):
    """ Wrapper of animation function
    """
    return FuncAnimation(plt.gcf(), animate, fargs=(cryptocurrency, currency,), interval=1000)


if __name__ == "__main__" : 

    # Test of all wrapper
    print(get_crypto_price(cryptocurrency='BTC', currency='USD'))
    print(get_cryptos_prices(['BTC', 'ETH'], ['EUR', 'GBP']))
    print(get_exchange_cypto_price(cryptocurrency='BTC', currency='USD', exchange=''))
    print(get_exchange_cypto_price(cryptocurrency='BTC', currency='USD', exchange='Binance'))

    # Test of function annimation
    plt.style.use('seaborn')
    x_vals = []
    y_vals = []
    ani = func_animation('BTC', 'USD')
    plt.show()

