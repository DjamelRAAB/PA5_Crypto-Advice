# 5th year project
## Application name : Crypto-Advice 
The topic of our 5th grade project is about crypto-currencies. The goal of this project is to extract information from historical crypto-currency data to provide advice to users based on the real-time price of crypto-currencies.
___


## CryptoAdvice API
In this project the API serves the data in JSON format and the actual useful payload is in an array of dictionaries. 
The response of our api can be used for time series analysis, price alarming script and even for creation of trading bot.

### Call the API to get data
How to call our API? 

* The API call consists of three parts,
    * First is baseurl :
        * http://cryptoadvice.com/
    * Second are the route :
        * /prediction/price
        * /prediction/sentiment
        * /tweets
        * /metrics    
    * Final part are the parameters that we provide for the call to choose the coin, for example: 
        * coin=BTC

## CryptoAdvice APP

___
