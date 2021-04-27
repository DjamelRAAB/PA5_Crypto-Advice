# 5th year project
## Application name : Crypto-Advice 
The topic of our 5th grade project is about crypto-currencies. The goal of this project is to extract information from historical crypto-currency data to provide advice to users based on the real-time price of crypto-currencies.
___


## Data (cryptocompare API)
In this project we will be calling cryptocompare.com API to get Bitcoin, Ethereum (or any cryptocurrency) historical price data and real-time price. The API serves the data in JSON format and the actual useful payload is in an array of dictionaries. 
We will provide tools to visualize the historical cryptocurrency price data via python library, and we will use that historical data for time series analysis, price alarming script and even for creation of trading bot.

### Call the API to get data
How to call the cryptocompare.com API? 

* The API call consists of two parts,
    * First is baseurl :
        * Historical data : https://min-api.cryptocompare.com/data/v2/histo{$frequence day\hour\minute}
        * Real time data : https://min-api.cryptocompare.com/data/price
    * Second are parameters that we provide for the call : fsym=BTC&tsyms=USD

1. Using requests package, example full API call for real time data : https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD

2. Useing function provided by cruptocompare package such as `cryptocompare.get_price('BTC', currency='USD', full=True)
`

___