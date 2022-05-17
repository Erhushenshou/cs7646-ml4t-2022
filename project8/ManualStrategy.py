import pandas as pd
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt
from util import get_data
import marketsimcode
import indicators
#class
    #def


def author():
    return 'twu411'


def testPolicy(symbol, sd, ed, sv=100000):

    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates, addSPY=True, colname='Adj Close')
    prices = prices_all[symbol]


    days = 10

    sma = indicators.sma(prices, days)
    sma_id = sma/prices - 1
    bb = indicators.bollingerband(prices, days)
    #b = bb['lowerband']
    #a = (prices - bb['lowerband'])
    #bbp = (sma - bb['lowerband']) / (bb['upperband'] - bb['lowerband'])
    momentum = indicators.get_momentum(prices, days)

    holdings = pd.DataFrame(np.nan, index=prices.index, columns=['holds'])

    for i in range(prices.shape[0]):
        if sma_id.iloc[i] < -0.003 and bb.iloc[i] < 0.2 and momentum.iloc[i] > -0.02:
            holdings.iloc[i] = 1000
        elif sma_id.iloc[i] > 0.00 and bb.iloc[i] > -0.35 and momentum.iloc[i] < 0.015:
            holdings.iloc[i] = -1000

    holdings.ffill(inplace=True)
    holdings.fillna(0, inplace=True)
    trades = holdings.diff()
    if holdings.iloc[0].values == 0:
        trades.iloc[0] = 0
    else:
        trades.iloc[0] = holdings.iloc[0]

    df_trades = pd.DataFrame(data=trades.values, index=trades.index, columns=['Shares'])

    # 


    return df_trades

def msploter(): #plot all the charts required in the mannual strategy section

    istrades = testPolicy('JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000)

    long = istrades[istrades>0]
    long.dropna(inplace=True)
    short = istrades[istrades<0]
    short.dropna(inplace=True)
    df_trades = pd.DataFrame(data=istrades.values, index=istrades.index, columns=['Shares'])
    is_ms_portval = marketsimcode.compute_portvals(orders=df_trades, start_val=100000, commission=9.95,
                                                   impact=0.005)


    bm_holdings = pd.DataFrame(np.nan, index=is_ms_portval.index, columns=['Shares'])
    bm_holdings.fillna(0, inplace=True)
    bm_trades = bm_holdings.diff()
    bm_trades.iloc[0] = 1000
    bm_trades.iloc[-1] = -1000
    bm_is_portval = marketsimcode.compute_portvals(orders=bm_trades, commission=9.95, impact=0.005, start_val=100000)

    is_ms_portval = pd.concat([is_ms_portval, bm_is_portval], axis=1)
    is_ms_portval.columns = ['manual strategy','benchmark']
    is_ms_portval= is_ms_portval/is_ms_portval.iloc[0]


    ax = is_ms_portval.plot(title='Manual Strategy in-sample Portfolio', fontsize=12, color=['red','purple'])
    ax.set_xlabel('Dates')
    ax.set_ylabel('Normalized Price')
    for i in (long.index):
        plt.axvline(x=i, color='b')
    for j in (short.index):
        plt.axvline(x=j, color='black')
    plt.savefig('.//images//ms insample chart.png')
    plt.close()

    #second chart(out of sample)
    ostrades = testPolicy('JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)

    long = ostrades[ostrades>0]
    long.dropna(inplace=True)
    short = ostrades[ostrades<0]
    short.dropna(inplace=True)
    os_df_trades = pd.DataFrame(data=ostrades.values, index=ostrades.index, columns=['Shares'])
    os_ms_portval = marketsimcode.compute_portvals(orders=os_df_trades, start_val=100000, commission=9.95,
                                                   impact=0.005)

    osbm_holdings = pd.DataFrame(np.nan, index=os_ms_portval.index, columns=['Shares'])
    osbm_holdings.fillna(0, inplace=True)
    osbm_trades = osbm_holdings.diff()
    osbm_trades.iloc[0] = 1000
    osbm_trades.iloc[-1] = -1000
    bm_os_portval = marketsimcode.compute_portvals(orders=osbm_trades, commission=9.95, impact=0.005, start_val=100000)


    os_ms_portval = pd.concat([os_ms_portval, bm_os_portval], axis=1)
    os_ms_portval.columns = ['manual strategy','benchmark']
    os_ms_portval= os_ms_portval/os_ms_portval.iloc[0]

    bx = os_ms_portval.plot(title='Manual Strategy out-of-sample Portfolio', fontsize=12, color=['red', 'purple'])
    bx.set_xlabel('Dates')
    bx.set_ylabel('Normalized Price')
    for i in (long.index):
        plt.axvline(x=i, color='b')
    for j in (short.index):
        plt.axvline(x=j, color='black')
    plt.savefig('.//images//ms outofsample chart.png')
    plt.close()

def dailyreturns(df):
    # quoted from 1-4
    dr = df.values
    dr = df/df.shift(1) - 1

    dr.iloc[0] = 0
    return dr







