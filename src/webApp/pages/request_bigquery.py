# google-cloud-bigquery
from google.cloud import bigquery
import pandas
client = bigquery.Client()
QUERY = (
    'SELECT * FROM `pa5-crypto-advice2.pa5_dataset.coin_prices` '
)  
query_job = client.query(QUERY).result().to_dataframe()
print(query_job.info())