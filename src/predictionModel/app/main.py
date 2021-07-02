from neuralnet import *
from utils import *
from pickle import dump
from pickle import load
import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage
# Imports the Google Cloud client library
from google.cloud import storage


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )


# The name for the new bucket
bucket_name = "pa5bucket"

source_blob_name="models/btc_scaler.pkl"
destination_file_name="/volume/"+source_blob_name
download_blob(bucket_name, source_blob_name, destination_file_name)

source_blob_name=destination_file_name="models/model_btc.pth"
destination_file_name="/volume/"+source_blob_name
download_blob(bucket_name, source_blob_name, destination_file_name)


# Explicitly create a credentials object. This allows you to use the same
# credentials for both the BigQuery and BigQuery Storage clients, avoiding
# unecessary API calls to fetch duplicate authentication tokens.
credentials, your_project_id = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Make clients.
BQ_CLIENT = bigquery.Client(credentials=credentials, project=your_project_id,)
BQ_STORAGE_CLIENT = bigquery_storage.BigQueryReadClient(credentials=credentials)
#const


#-----------train------------------------------------
'''
START_DATE=datetime.now()
END_DATE=datetime(2021,6,14)
CRYPTO='BTC'
PATH_BTC="/home/jbouhadoun/Téléchargements/btc_bis.csv"
PATH_MODEL_BTC=""
PATH_scaler_BTC=""

df=get_data(START_DATE,END_DATE,CRYPTO)
df1=read_csv(PATH_BTC)
#df_merge=merge_data(df,df1)
train_data,test_data=split_data(df_merge,0.999)
train_normalized,scaler = normalize_data(train_data)
train_loader=create_data_loader(train_normalized)
test_loader=create_data_loader_test(test_data[-10:],scaler)
'''
#---------------------------------------------------------------
#-------------------------------------predict-------------------

#data={"1623715200000":{"high":41307.06,"low":39526.69,"open":40526.63,"volumefrom":48248.1,"volumeto":1943860792.1199998856,"close":40161.86,"addresses_active_count":982683,"addresses_new_non_zero_count":442413,"addresses_count":842701203,"addresses_receiving_count":677272,"addresses_sending_count":579548,"transactions_transfers_volume_sum":1402938.6358141699,"mining_hash_rate_mean":"128092375116985000000","mining_difficulty_latest":"85610685580095700000000","sentiment_analysis":0.0617420522}}
#data = s.get_json()

list_coin=['BTC']
for coin in list_coin:
    dataframe=get_data_predict(BQ_CLIENT,BQ_STORAGE_CLIENT,coin)
    prediction=set_predictions(coin,BQ_CLIENT,dataframe)



