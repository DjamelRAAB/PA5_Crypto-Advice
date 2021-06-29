from scrap import scrap
import json
import pandas as pd
from google.cloud import pubsub_v1
import os
import ast
import datetime
from datetime import timezone
import time

today=datetime.date.today().strftime("%Y-%m-%d")
tomorow = (datetime.date.today() + datetime.timedelta(1)).strftime("%Y-%m-%d")

project_id = os.environ['project_id']
topic_id = os.environ['topic_id']
key_words_btc = ["BTC","bitcoin"]
key_words_eth = ["ETH","etherum","ether"]

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


data = scrap(words=key_words_btc, start_date=today , max_date=tomorow ,interval=1,lang="en",headless=True, resume=False)
data["time"]= data["time"].apply(lambda x: x[:10])


#---------TO HISTORYY-------------------------------------------------
#data=pd.read_csv("/app/outputs/historical_tweet_eth_final_timestamp.csv")   #|
#'------------------dhistory---------------------------------------
data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d")
data['time'] = data['time'].apply(lambda x: int(x.replace(tzinfo=timezone.utc).timestamp()))
data = data.to_json(orient="records")
dictionary=json.loads(data)


#dictionary = ast.literal_eval(data)
for elt in dictionary :
	future = publisher.publish(topic_path, json.dumps(elt).encode())
	print(future.result())


'''
data = scrap(words=key_words_eth, start_date=today , max_date=tomorow ,interval=1,lang="en",headless=True, resume=False)
data["time"]= data["time"].apply(lambda x: x[:10])
data = data.to_json(orient="records")
dictionary = ast.literal_eval(data)
for elt in dictionary :
	future = publisher.publish(topic_path, json.dumps(elt).encode())
	print(future.result())'''

