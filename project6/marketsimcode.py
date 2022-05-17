""""""
"""MC2-P1: Market simulator.  		  	   		  	  			  		 			     			  	 

Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  	  			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  	  			  		 			     			  	 
All Rights Reserved  		  	   		  	  			  		 			     			  	 

Template code for CS 4646/7646  		  	   		  	  			  		 			     			  	 

Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  	  			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  	  			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  	  			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  	  			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  	  			  		 			     			  	 
or edited.  		  	   		  	  			  		 			     			  	 

We do grant permission to share solutions privately with non-students such  		  	   		  	  			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  	  			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  	  			  		 			     			  	 
GT honor code violation.  		  	   		  	  			  		 			     			  	 

-----do not edit anything above this line---  		  	   		  	  			  		 			     			  	 

Student Name: Tucker Balch (replace with your name)  		  	   		  	  			  		 			     			  	 
GT User ID: twu411 (replace with your User ID)  		  	   		  	  			  		 			     			  	 
GT ID: 596568372 (replace with your GT ID)  		  	   		  	  			  		 			     			  	 
"""

import datetime as dt
import os
import matplotlib.pyplot as plt
import numpy as np
import TheoreticallyOptimalStrategy as tos
import pandas as pd
from util import get_data
import matplotlib



orders = tos.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv=100000)

def compute_portvals(orders= orders, start_val=100000.0,commission=0.0,impact=0.00):

    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    orderdata = orders
    orderdata = orderdata.sort_index()
    # orderdata.fillna(method='ffill', inplace=True)
    # orderdata.fillna(method='bfill', inplace=True)
    start_date = orderdata.index.min()
    end_date = orderdata.index.max()
    orderdata.insert(0, 'Symbol','JPM' )
    orderdata.insert(1, 'Order', 'SELL')
    for i in range(orderdata.shape[0]):
        if orderdata.iloc[i, 2] > 0:
            orderdata.iloc[i, 1] = 'BUY'
    orderdata['Shares'] = orderdata['Shares'].abs()
    orderdata = orderdata.loc[(orderdata.Shares != 0)]

    cash = start_val
    buyingtable = get_data(orderdata['Symbol'].unique().tolist(), pd.date_range(start_date, end_date), addSPY=False)
    buyingtable.index.name = 'Date'
    # print(buyingtable)
    buyingtable = buyingtable.dropna(axis=0, how='any')
    holdingtable = buyingtable.copy()
    holdingtable[:] = 0
    holdingtable['cash'] = start_val
    holdingtable['portval'] = start_val
    # buyingtable.fillna(method='ffill', inplace=True)
    # buyingtable.fillna(method='bfill', inplace=True)

    # print(holdingtable)

    for i in range(orderdata.shape[0]):
        purchasedate = orderdata.index[i]
        symbol = orderdata.iloc[i, 0]
        option = orderdata.iloc[i, 1]
        shares = orderdata.iloc[i, 2]
        # thisdatafile = pd.read_csv(os.path.join(os.environ.get("MARKET_DATA_DIR", "../data/"), "{}.csv".format(str(symbol))))
        # thisdatafile = thisdatafile.set_index('Date') #date as index
        price = buyingtable.loc[purchasedate, symbol]
        # print(thisdatafile)
        # print(price)
        # print(price * shares)

        if option == 'BUY':

            holdingtable.loc[purchasedate, 'cash'] = holdingtable.loc[purchasedate, 'cash'] - shares * price * (
                        1 + impact) - commission
            holdingtable.loc[purchasedate, symbol] = holdingtable.loc[purchasedate, symbol] + shares
        else:

            holdingtable.loc[purchasedate, 'cash'] = holdingtable.loc[purchasedate, 'cash'] + shares * price * (
                        1 - impact) - commission
            holdingtable.loc[purchasedate, symbol] = holdingtable.loc[purchasedate, symbol] - shares
        holdingtable.loc[purchasedate:, 'cash'] = holdingtable.loc[purchasedate, 'cash']
        holdingtable.loc[purchasedate:, symbol] = holdingtable.loc[purchasedate, symbol]
    holdingtable.loc[:, 'portval'] = (holdingtable.iloc[:, range(0, buyingtable.shape[1])] * buyingtable).sum(
        axis=1) + holdingtable.loc[:, 'cash']

    # print(holdingtable.iloc[:, range(0, buyingtable.shape[1])])

    # print(holdingtable)
    # print(buyingtable)
    portvals = holdingtable.loc[:, 'portval']
    # print(portvals)

    # portvals = get_data(["IBM"], pd.date_range(start_date, end_date))
    # portvals = portvals[["IBM"]]  # remove SPY
    # rv = pd.DataFrame(index=portvals.index, data=portvals.values)

    # return rv
    return portvals


def author():
    return 'twu411'


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    """DO NOT use in code submitted for grading"""



def test_code():
    """
    Helper function to test code
    """
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-02.csv"
    sv = 100000

    # Process orders
    portvals = compute_portvals(orders, start_val=sv)
    #print(portvals)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

        # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    '''
    start_date = dt.datetime(2008, 1, 1)  		  	   		  	  			  		 			     			  	 
    end_date = dt.datetime(2008, 6, 1)  		  	   		  	  			  		 			     			  	 
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [  		  	   		  	  			  		 			     			  	 
        0.2,  		  	   		  	  			  		 			     			  	 
        0.01,  		  	   		  	  			  		 			     			  	 
        0.02,  		  	   		  	  			  		 			     			  	 
        1.5,  		  	   		  	  			  		 			     			  	 
    ]  		  	   		  	  			  		 			     			  	 
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [  		  	   		  	  			  		 			     			  	 
        0.2,  		  	   		  	  			  		 			     			  	 
        0.01,  		  	   		  	  			  		 			     			  	 
        0.02,  		  	   		  	  			  		 			     			  	 
        1.5,  		  	   		  	  			  		 			     			  	 
    ]  		  	   		  	  			  		 			     			  	 

    # Compare portfolio against $SPX  		  	   		  	  			  		 			     			  	 
    print(f"Date Range: {start_date} to {end_date}")  		  	   		  	  			  		 			     			  	 
    print()  		  	   		  	  			  		 			     			  	 
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		  	  			  		 			     			  	 
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		  	  			  		 			     			  	 
    print()  		  	   		  	  			  		 			     			  	 
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		  	  			  		 			     			  	 
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		  	  			  		 			     			  	 
    print()  		  	   		  	  			  		 			     			  	 
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		  	  			  		 			     			  	 
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		  	  			  		 			     			  	 
    print()  		  	   		  	  			  		 			     			  	 
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		  	  			  		 			     			  	 
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		  	  			  		 			     			  	 
    print()  		  	   		  	  			  		 			     			  	 
    print(f"Final Portfolio Value: {portvals[-1]}")  	
 
    sd=dt.datetime(2008, 1, 1)
    ed=dt.datetime(2009,12,31)
    dates = pd.date_range(sd, ed)
    bm = get_data(['JPM'], dates, addSPY=False, colname='Adj Close')
    combined = bm.join(portvals, how='outer')
    combined.dropna(inplace=True)
    combined = combined/combined.ix[0, :]
    normedbench = combined.ix[:, 0]
    normedport = combined.ix[:, 1]

    #print(normedbench)

    plt.figure(figsize=(12,6.5))
    plt.plot(normedport, label="Portfolio", color='red')
    plt.plot(normedbench, label="Benchmark", color='purple')

    plt.xlabel('Date')
    plt.ylabel('Normalized Prices')
    plt.legend()
    plt.grid(True)
    plt.title("Theoretically Optimial Strategy for JPM")
    plt.savefig(".//images//JPM tos.png")
    plt.close()
    '''


if __name__ == "__main__":


    test_code()


