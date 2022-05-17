import random
import pandas as pd
import StrategyLearner as sl
import ManualStrategy as ms
import marketsimcode
from util import get_data
import datetime as dt
import experiment1
import experiment2
random.seed(596568372)
sd = dt.datetime(2008,1,1)           #in sample starting time
ed = dt.datetime(2009,12,31)         #in sample ending time
dates = pd.date_range(sd, ed)
symbol = 'JPM'                       #targeted stock symbol

sd_os=dt.datetime(2010, 1, 1)        #out-of sample starting time
ed_os=dt.datetime(2011,12,31)        #out-of sample ending time

prices_all = get_data([symbol], dates, addSPY=True, colname='Adj Close')
prices = prices_all[symbol]

experiment1.is_compare(symbol, sd=sd, ed=ed, ifreturn=True)
experiment1.os_compare(symbol, sd=sd_os, ed=ed_os, ifreturn=True)
print(experiment2.impact(symbol, sd=sd, ed=ed))
ms.msploter()



def author():
    return 'twu411'
