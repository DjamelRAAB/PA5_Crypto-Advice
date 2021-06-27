import json
import pandas as pd
from google.cloud import pubsub_v1
import os
import ast
import datetime
import cryptocompare

def get_data(start_date,crypto):

	data = cryptocompare.get_historical_price_day(crypto, 'USD', limit=1, exchange='CCCAGG', toTs=start_date)

	df = pd.DataFrame.from_dict(data)
	df=df.iloc[:,:7]
	df["coin"] = crypto
	return df.to_json(orient="records")



if __name__ == "__main__" :  

	project_id = os.environ['project_id']
	topic_id = os.environ['topic_id']

	publisher = pubsub_v1.PublisherClient()
	topic_path = publisher.topic_path(project_id, topic_id)

	today=datetime.datetime.today()

	data = get_data(today,"BTC")
	print(data)
	dictionary = json.loads(data)
	for elt in dictionary :
		future = publisher.publish(topic_path, json.dumps(elt).encode())
		print(future.result())

	data = get_data(today,"ETH")
	dictionary = json.loads(data)
	for elt in dictionary :
		future = publisher.publish(topic_path, json.dumps(elt).encode())
		print(future.result())
