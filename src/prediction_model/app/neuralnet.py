import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime 
from sklearn import preprocessing
import torch
import torch.nn as nn
from torch.optim import Adam
import torch.utils.data as data_utils 


class NeuralNet(nn.Module):
    def __init__(self, 
                 activation_function = nn.ReLU,
                 optimizer = Adam,
                 dropout = 0.2
                ):
        super(NeuralNet, self).__init__()
        input_dim = 13
        hidden_dim = 100
        output_dim = 1
        self.lstm1 = nn.LSTM(input_dim, hidden_dim)
        self.dropout1 = nn.Dropout(p = dropout)
        self.lstm2 = nn.LSTM(hidden_dim, hidden_dim)
        self.layers =[nn.Dropout(p = dropout)]
        self.layers.append(nn.Linear(hidden_dim, output_dim))
        self.layers = nn.Sequential(*self.layers)
        


    def forward(self, x):
        out, _ = self.lstm1(x.view(len(x), 1 , -1))
        out = self.dropout1(out.view(len(x), -1))
        out, _ = self.lstm2(out.view(len(x), 1 , -1))
        out = self.layers(out.view(len(x), -1))
        return out




