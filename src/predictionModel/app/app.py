import pickle
# Import all the packages you need for your model below
import numpy as np
import pandas as pd
from pickle import dump
from pickle import load
import sys
# Import Flask for creating API
from flask import Flask, request, jsonify
import json
import requests
from utils import *
from neuralnet import *
import torch

# Load the trained model from current directory
#with open('./model_btc.pkl', 'rb') as model_pkl:
    #knn = pickle.load(model_pkl)

# Initialise a Flask app
app = Flask(__name__)

# Create an API endpoint
@app.route('/predict',methods=['GET', 'POST', 'DELETE', 'PUT'])
def predict_iris():
    # Read all necessary request parameters
    data = request.get_json()
    dataframe = pd.DataFrame.from_dict(data,orient="index")
    model= torch.load("/volume/model_btc.pth")
    scaler= load(open('/volume/btc_scaler.pkl', 'rb'))
    test_loader_today=create_data_loader_test(dataframe,scaler)
    s=predict(model,test_loader_today,scaler)







    
    # return the result back
    return jsonify(predicted_price=s[0])

'''example de requette
curl -X POST -H 'Content-Type: application/json' http://0.0.0.0:8080/predict -d'{"1623715200000":{"high":41307.06,"low":39526.69,"open":40526.63,"volumefrom":48248.1,"volumeto":1943860792.1199998856,"close":40161.86,"addresses_active_count":982683,"addresses_new_non_zero_count":442413,"addresses_count":842701203,"addresses_receiving_count":677272,"addresses_sending_count":579548,"transactions_transfers_volume_sum":1402938.6358141699,"mining_hash_rate_mean":"128092375116985000000","mining_difficulty_latest":"85610685580095700000000","sentiment_analysis":0.0617420522}}'


'''
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
    