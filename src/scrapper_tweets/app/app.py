
# Import Flask for creating API
from flask import Flask, request, jsonify
from functions import *
from scrap import *
import json
import pandas as pd

# Load the trained model from current directory
#with open('./model_btc.pkl', 'rb') as model_pkl:
    #knn = pickle.load(model_pkl)

# Initialise a Flask app
app = Flask(__name__)

# Create an API endpoint
@app.route('/scrap',methods=['GET', 'POST', 'DELETE', 'PUT'])
def scraping():
    # Read all necessary request parameters
    data = request.get_json()
    print(type(data['words']))
    s=data['words']

    data = scrap(words=data['words'], start_date=data["start_date"], max_date=data["max_date"],interval=1,lang="en",headless=True, resume=False)
    req=data.to_json(orient="index")


  
    # return the result back
    return req

'''example de requette
curl -X POST -H 'Content-Type: application/json' http://0.0.0.0:8080/scrap -d'{"words": ["btc","bitcoin"],"start_date": "2021-06-24","max_date": "2021-06-25"}'
'''
if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')