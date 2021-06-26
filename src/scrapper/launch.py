from scrap import scrap
import json
import pandas as pd
from google.cloud import pubsub_v1
import os

project_id = os.environ['project_id']
topic_id = os.environ['topic_id']

data = scrap(words=["btc","bitcoin"], start_date="2021-06-24", max_date="2021-06-25",interval=1,lang="en",
	headless=True, resume=False).to_json(orient="records")

print(data[1:-1])
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
future = publisher.publish(topic_path, data.encode())
print(future.result())