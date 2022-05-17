import numpy as np
import pandas as pd
from util import get_data, symbol_to_path
import datetime as dt
import matplotlib.pyplot as plt
import indicators as id
import TheoreticallyOptimalStrategy as tos
import marketsimcode as ms
df_trades = tos.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)


start_date = dt.datetime(2008, 1, 1)
end_date = dt.datetime(2009, 12, 31)
stock = ['JPM']
df = get_data(stock,pd.date_range(start_date, end_date), addSPY=False)
df = df.dropna()

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):

    """Plot stock prices with a custom title and meaningful axis labels."""
    """DO NOT use in code submitted for grading"""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
def author():
    return 'twu411'

portvals = ms.compute_portvals(df_trades, start_val=100000)

sd=dt.datetime(2008, 1, 1)
ed=dt.datetime(2009,12,31)
dates = pd.date_range(sd, ed)
bm = get_data(['JPM'], dates, addSPY=False, colname='Adj Close')
combined = bm.join(portvals, how='outer')
combined.dropna(inplace=True)
combinednorm = combined/combined.ix[0, :]
normedbench = combined.ix[:, 0]
normedport = combined.ix[:, 1]

#print(combined)
#print(normedbench)
ax = combinednorm.plot(title= 'Theoretically Optimal Strategy for JPM', fontsize=12, color=['purple', 'red'])
ax.set_xlabel('Date')
ax.set_ylabel('Normalized Price')
plt.savefig(".//images//JPM tos.png")
plt.show()

plt.close()

def cal_dailyreturns(df):
    #quoted from 1-4
    dr = df/df.shift(1) - 1
    dr.ix[0] = 0
    return dr
dr = cal_dailyreturns(combinednorm)
dr_mean = dr.mean(axis=0)
dr_std = dr.std(axis=0)
#print(dr)
cr = (combinednorm.ix[-1]/ combinednorm.ix[0]) - 1

print(dr_mean, dr_std, cr)

id.sma(df, 10, plot=True, combine=True)
id.bollingerband(df, 30, plot=True, combine=True)
id.get_momentum(df, 10, plot=True)
id.PPI(df, plot=True)
id.GoldenCross(df, 5, 20, plot=True)

EMA12 = id.EMA(df, 12)
EMA26 = id.EMA(df, 26)
EMA = pd.concat([EMA12, EMA26], axis=1)
EMA.columns = ['EMA12', 'EMA26']
plot_data(EMA, title="EMA 12 vs EMA26", xlabel="Date", ylabel="EMA Prices")
plt.savefig(".//images//EMA.png")
plt.show()

plt.close()