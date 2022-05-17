import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from util import get_data



def testPolicy(symbol, sd, ed, sv=100000.0):
    ## this policy is like this: buy when the price will go up the next day, sell when the price will do down the next day
    # get price data
    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates, addSPY=True, colname='Adj Close')
    prices = prices_all[symbol]  # only portfolio symbols
    # prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # detect price changes
    #pricesdiff = prices.diff()

    pricesdiff = prices *2

    for i in range(prices.shape[0] - 1):
        #date = prices.index[i]
        pricesdiff.iloc[i+1] = prices.iloc[i+1] - prices.iloc[i]
    pricesdiff[0] = np.nan


    #print(pricesdiff)


    action = np.sign(pricesdiff.shift(-1)) * 1000
    #print(action)
    trades = action * 2
    for i in range(action.shape[0] - 1):
        trades.iloc[i+1] = action.iloc[i+1] - action.iloc[i]
    trades[0] = np.nan
    trades.iloc[0] = action[0]
    trades.iloc[-1] = 0
    trades.columns = 'Shares'


    # buy and sell happens when the difference change direction
    df_trades = pd.DataFrame(data=trades.values, index = trades.index, columns = ['Shares'])

    return df_trades

def author():
    return 'twu411'

orders = testPolicy('JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))


