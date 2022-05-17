
import pandas as pd
import StrategyLearner as sl
import marketsimcode
import datetime as dt
from matplotlib import pyplot as plt

def impact(symbol,sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31)):
    impactlist = [0, 0.001, 0.005, 0.01, 0.05, 0.1]
    portfoliolist = []
    for i in impactlist:
        sl_learner = sl.StrategyLearner(verbose = False, impact = i, commission=9.95) # constructor
        sl_learner.add_evidence(symbol = symbol, sd=sd, ed=ed, sv = 100000) # training phase
        os_sl_df_trades = sl_learner.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = 100000) # testing phase
        os_sl_portval = marketsimcode.compute_portvals(orders=os_sl_df_trades, start_val=100000, commission=0, impact=i, sym=symbol)
        portfoliolist.append(os_sl_portval)


    combined = pd.concat(portfoliolist, axis=1)
    combined = combined/combined.iloc[0]
    combined.columns = ['impact 0','impact 0.001','impact 0.005','impact 0.01','impact 0.05', 'impact 0.1']

    ax = combined.plot(title='In-sample Portfolio under different impact values', fontsize=12)
    ax.set_xlabel('Dates')
    ax.set_ylabel('Normalized Price')
    plt.savefig('.//images//impact variation.png')
    plt.close()

    std = combined.std(axis=0)
    cr = combined.iloc[-1] - combined.iloc[0]


    return 'std = {}'.format(std), 'cumulative returns ={}'.format(cr)

def author():
    return 'twu411'