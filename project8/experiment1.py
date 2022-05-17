import numpy as np
import pandas as pd
import StrategyLearner as sl
import ManualStrategy as ms
import marketsimcode
from util import get_data
import datetime as dt
import random
from matplotlib import pyplot as plt

def is_compare(symbol,sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), ifreturn=False):

    sl_learner = sl.StrategyLearner(verbose = False, impact = 0.005, commission=9.95) # constructor
    sl_learner.add_evidence(symbol = symbol, sd=sd, ed=ed, sv = 100000) # training phase
    is_sl_df_trades = sl_learner.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = 100000) # testing phase

    is_sl_portval = marketsimcode.compute_portvals(orders=is_sl_df_trades, start_val=100000, commission=9.95, impact=0.005, sym=symbol)


    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    dates = pd.date_range(sd, ed)

    prices_all = get_data([symbol], dates, addSPY=True, colname='Adj Close')
    prices = prices_all[symbol]


    bm_holdings = pd.DataFrame(np.nan, index=prices.index, columns=['Shares'])
    bm_holdings.fillna(0, inplace=True)
    bm_trades = bm_holdings.diff()
    bm_trades.iloc[0] = 1000
    bm_trades.iloc[-1] = -1000
    bm_is_portval = marketsimcode.compute_portvals(orders=bm_trades, commission=9.95, impact=0.005, start_val=100000, sym=symbol)
    #print(bm_is_portval) #in sample benchmark portvals


    #mannul strategy portval
    ms_is_df_trades = ms.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
    is_ms_portval = marketsimcode.compute_portvals(orders=ms_is_df_trades, start_val=100000, commission=9.95, impact=0.005, sym=symbol)

    #combine three portval

    is_portval = pd.concat([is_sl_portval, bm_is_portval, is_ms_portval], axis=1, join='inner')
    norm_is_portval = is_portval/100000
    columns = ['strategy learner', 'benchmark', 'manual strategy']
    norm_is_portval.columns = columns

    ax = norm_is_portval.plot(title='In-Sample Comparison', fontsize=12)
    ax.set_xlabel('Dates')
    ax.set_ylabel('Normalized Price')
    plt.savefig('.//images//in-sample comparison.png')
    plt.close()

    if ifreturn==True:
        is_cr = norm_is_portval.iloc[-1] - norm_is_portval.iloc[0]
        is_dr = ms.dailyreturns(norm_is_portval)
        print('is_dr.std=', is_dr.std(axis=0))
        print('is_dr.mean=', is_dr.mean(axis=0))
        print('is_cr=', is_cr)






        #return is_dr, is_cr

def os_compare(symbol,sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), ifreturn=False):
    random.seed(596568372)

    sl_learner = sl.StrategyLearner(verbose = False, impact = 0.005, commission=9.95) # constructor
    sl_learner.add_evidence(symbol = symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000) # training phase
    os_sl_df_trades = sl_learner.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = 100000) # testing phase

    os_sl_portval = marketsimcode.compute_portvals(orders=os_sl_df_trades, start_val=100000, commission=9.95, impact=0.005, sym=symbol)


    #out of sample benchmark
    sd_os=sd
    ed_os=ed
    os_dates = pd.date_range(sd_os, ed_os)
    os_prices_all = get_data([symbol], os_dates, addSPY=True, colname='Adj Close')
    os_prices = os_prices_all[symbol]

    os_bm_holdings = pd.DataFrame(np.nan, index=os_prices.index, columns=['Shares'])
    os_bm_holdings.fillna(0, inplace=True)
    os_bm_trades = os_bm_holdings.diff()
    os_bm_trades.iloc[0] = 1000
    os_bm_trades.iloc[-1] = -1000

    bm_os_portval = marketsimcode.compute_portvals(orders=os_bm_trades, commission=9.95, impact=0.005, start_val=100000, sym=symbol)
    #print(bm_os_portval) #in sample benchmark portvals

    #mannual strategy portvals:

    ms_os_df_trades = ms.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
    os_ms_portval = marketsimcode.compute_portvals(orders=ms_os_df_trades, start_val=100000, commission=9.95, impact=0.005, sym=symbol)

    os_portval = pd.concat([os_sl_portval, bm_os_portval, os_ms_portval], axis=1, join='inner')
    norm_os_portval = os_portval/100000
    columns = ['strategy learner', 'benchmark', 'manual strategy']
    norm_os_portval.columns = columns

    ax = norm_os_portval.plot(title='Out-of-Sample Comparison', fontsize=12)
    ax.set_xlabel('Dates')
    ax.set_ylabel('Normalized Price')
    plt.savefig('.//images//out-of-sample comparison.png')
    plt.close()



    if ifreturn==True:
        os_cr = norm_os_portval.iloc[-1] - norm_os_portval.iloc[0]
        os_dr = ms.dailyreturns(norm_os_portval)
        print('os_dr.std=', os_dr.std(axis=0))
        print('os_dr.mean=', os_dr.mean(axis=0))
        print('os_cr=', os_cr)


def author():
    return 'twu411'