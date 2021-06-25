from scrap import scrap
import json
import pandas as pd

data = scrap(words=["btc","bitcoin"], start_date="2021-06-24", max_date="2021-06-25",interval=1,lang="en",
	headless=True, resume=False)

'''
f = open('juju.json')
data = json.loads(f.read())
dataframe = pd.DataFrame.from_dict(data,orient="index")

print(dataframe)'''