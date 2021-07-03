from neuralnet import *
import pandas as pd
import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage
from pickle import dump
from pickle import load

BASE_PATH = "/volume/models"
torch.manual_seed(42)
torch.cuda.manual_seed(42)
np.random.seed(42)
torch.backends.cudnn.deterministic=True

def read_csv(PATH):
    df=pd.read_csv(PATH)
    df=df.fillna(df.mean())
    df=df.iloc[:,1:]
    return df
    
# get Data api crypto compare 
def get_data(start_date,end_date,crypto):
    l=[]
    i=0

    while start_date>=end_date:
        i=i+1
        print("requette :",i)
        try : 
            data = cryptocompare.get_historical_price_day(crypto, 'USD', limit=2000, exchange='CCCAGG', toTs=start_date)
            if data is None : 
                raise ValueError 
        except: 
            break

        l=data+l
        start_date=datetime.fromtimestamp(data[0]['time'])
    df = pd.DataFrame.from_dict(l)
    df=df.iloc[:,:7]

def merge_data(df,df1):
    df_merge=pd.merge(df,df1,on="time")
    df_merge["time"]=pd.to_datetime(df_merge["time"], unit='s')
    df_merge = df_merge.set_index('time')
    df_merge.index = pd.to_datetime(df_merge.index, unit='s')
    return df_merge

def split_data(data, train_prop=100):
    train_data = data.iloc[:int(train_prop * len(data))]
    test_data = data.iloc[int(train_prop * len(data)):]
    return train_data, test_data

def normalize_data(traindf,min_max_scaler=None):
    x = traindf.values
    if min_max_scaler is None:
        min_max_scaler = preprocessing.MinMaxScaler()
        min_max_scaler.fit(x)
    x_scaled=min_max_scaler.transform(traindf.values)
    normalized_df = pd.DataFrame(x_scaled, columns = traindf.columns)
    return normalized_df,min_max_scaler

def plot_curves(train_data,test_data,to_plot, labels, title='', x_label='', y_label=''):
    fig, ax = plt.subplots(1, figsize=(14, 7))
    for i in range(len(to_plot)):
        ax.plot(to_plot[i], label=labels[i])
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()



def create_data_loader(train_normalized):
    train_target_tensor = torch.tensor(train_normalized['close'].values.astype(np.float64))
    train_data_tensor = torch.tensor(train_normalized.drop('close', axis = 1).values) 
    train_tensor = data_utils.TensorDataset(train_data_tensor, train_target_tensor) 
    train_loader = data_utils.DataLoader(dataset = train_tensor, batch_size = 32, shuffle = True)
    return train_loader



def create_data_loader_test(test_data,scaler):
    test_normalized,_ = normalize_data(test_data,scaler)
    test_target = torch.tensor(test_normalized['close'].values.astype(np.float64))
    test = torch.tensor(test_normalized.drop('close', axis = 1).values) 
    print(test_target[0])
    test_tensor = data_utils.TensorDataset(test, test_target) 
    test_loader = data_utils.DataLoader(dataset = test_tensor, batch_size = 32, shuffle = False)
    return test_loader


def model(train_loader,epochs=1000):
    model = NeuralNet()

    EPOCHS = epochs

    #target = pd.DataFrame(data = train_normalized['close'])


    criterion = nn.MSELoss()
    optimizer = Adam(model.parameters(), lr=0.0001)

    losses = []
    for epoch in range(EPOCHS):
        epoch_loss = 0
        for bidx, batch in tqdm(enumerate(train_loader)):
            X, Y = batch
            model.zero_grad()
            loss = 0
            for i in range(len(X)):
                x, y = X[i], Y[i]
                x = x.view(-1, len(x))

                #Forward Pass
                y_hat = model(x.float())

                #Loss
                loss += criterion(y.float(), y_hat.float())

            #Backward pass
            loss.backward()

            #Parameters optimization
            optimizer.step()

            epoch_loss += float(loss)

        losses.append(epoch_loss)
        model_close=model
        print("Epoch ", epoch, ": ", epoch_loss)
    return model


def predict(model,test_loader,scaler):
    y_list = []
    y_hat_list = []
    min_max_scaler=scaler
    for bidx, batch in tqdm(enumerate(test_loader)):
            X, Y = batch
            for i in range(len(X)):
                x, y = X[i], Y[i]
                x = x.view(-1, len(x))
                y_hat = model(x.float())
                
                print(y_hat)
                vmin = min_max_scaler.data_min_[5]
                vmax = min_max_scaler.data_max_[5]
                y_hat_list.append(float(y_hat)* (vmax - vmin) + vmin)
    return y_hat_list




def set_predictions(coin,bqclient,dataframe):
    #/volume/
    if coin =='BTC':
        model= torch.load(f"{BASE_PATH}/model_btc.pth")
        scaler= load(open(f'{BASE_PATH}/btc_scaler.pkl', 'rb'))
    if coin == 'ETH':
        model= torch.load(f"{BASE_PATH}/model_eth.pth")
        scaler= load(open(f'{BASE_PATH}/eth_scaler.pkl', 'rb'))
    test_loader_today=create_data_loader_test(dataframe,scaler)
    pred=predict(model,test_loader_today,scaler)[0]
    query_string = f"""
        INSERT INTO `pa5-crypto-advice2.pa5_dataset.coin_prices_predicted` (time, price, coin)
        VALUES
            ('2021-06-15 00:00:00 UTC', {pred}, '{coin}')
        """
    dataframe = (
        bqclient.query(query_string)
        .result()
    )

def get_data_predict(bqclient, bqstorageclient, coin : str = 'BTC') :
    # Download query results.
    query_string = query_string = f"""
    WITH tweets AS (
    SELECT time, coin, avg(sentiment_analysis) as sentiment_analysis
    FROM pa5-crypto-advice2.pa5_dataset.coin_tweets
    GROUP BY time, coin
    )
    SELECT DISTINCT  tweets.time as date ,
        tweets.coin ,
        price.high ,
        price.low ,
        price.open ,
        price.volumefrom ,
        price.volumeto ,
        price.close ,
        metrics.addresses_active_count ,
        metrics.addresses_new_non_zero_count ,
        metrics.addresses_count ,
        metrics.addresses_receiving_count ,
        metrics.addresses_sending_count ,
        metrics.transactions_transfers_volume_sum ,
        metrics.mining_hash_rate_mean ,
        metrics.mining_difficulty_latest ,
        tweets.sentiment_analysis
    FROM pa5-crypto-advice2.pa5_dataset.coin_glassnode_metrics as metrics
    JOIN tweets
    ON metrics.time = tweets.time 
    AND metrics.coin = tweets.coin
    JOIN pa5-crypto-advice2.pa5_dataset.coin_prices as price
    ON metrics.time = price.time 
    AND metrics.coin = price.coin
    WHERE tweets.coin = '{coin}' 
    ORDER BY date DESC
    LIMIT 1;
    """
    dataframe = (
        bqclient.query(query_string)
        .result()
        .to_dataframe(bqstorage_client=bqstorageclient)
    ).drop(columns=['date','coin'])
    print(dataframe)
    return dataframe