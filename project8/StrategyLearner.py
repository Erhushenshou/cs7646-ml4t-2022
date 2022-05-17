""""""  		  	   		  	  			  		 			     			  	 
"""  		  	   		  	  			  		 			     			  	 
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
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
import random
import indicators
  		  	   		  	  			  		 			     			  	 
import pandas as pd  		  	   		  	  			  		 			     			  	 
import util as ut
import matplotlib.pyplot as plt
import marketsimcode
import numpy as np
import RTLearner as rt
import BagLearner as bl
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
class StrategyLearner(object):  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  	  			  		 			     			  	 
        If verbose = False your code should not generate ANY output.  		  	   		  	  			  		 			     			  	 
    :type verbose: bool  		  	   		  	  			  		 			     			  	 
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  	  			  		 			     			  	 
    :type impact: float  		  	   		  	  			  		 			     			  	 
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  	  			  		 			     			  	 
    :type commission: float  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    # constructor  		  	   		  	  			  		 			     			  	 
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        Constructor method  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        self.verbose = verbose  		  	   		  	  			  		 			     			  	 
        self.impact = impact  		  	   		  	  			  		 			     			  	 
        self.commission = commission
        self.learner = None
        self.bags = 50
        self.leaf_size = 10
        self.YSELL = -0.05
        self.YBUY = 0.03
        self.days_y = 14
        self.day_sma = 10
        self.day_bb = 10
        self.day_m = 17
  		  	   		  	  			  		 			     			  	 
    # this method should create a QLearner, and train it for trading

    def Y_calculator(self, df, days, YSELL, YBUY, impact):

        #df = df.iloc[:,0]
        ret = df.shift(-1 * (days-1))/df - 1
        #print (ret)
        signals = pd.DataFrame(np.nan, index=ret.index, columns=['signal'])
        signals = ret
        '''


        signals[ret>=YBUY] = 1
        signals[ret<=YSELL] = -1
        signals[abs(signals) != 1] = 0
        
        '''
        for i in range(ret.shape[0]):
            if (ret.iloc[i].values>= YBUY * (20*impact+ 1)):
                signals.iloc[i] = 1
            elif (ret.iloc[i].values <= YSELL * (20*impact+ 1)):
                signals.iloc[i] = -1

            elif (ret.iloc[i].values >YSELL  * (20*impact+ 1) and ret.iloc[i].values <YBUY)  * (20*impact+ 1):
                signals.iloc[i] = 0

        #signals.ffill(inplace=True)
        #signals.fillna(0, inplace=True)




        return signals



    def X_factors(self, df_trades, day_sma, day_bb, day_m):
        #vectorize and combine X

        sma = indicators.sma(df_trades, day_sma)
        sma_id = sma / df_trades - 1
        bb = indicators.bollingerband(df_trades, day_bb)
        momentum = indicators.get_momentum(df_trades, day_m)

        X = pd.concat([sma_id, bb, momentum], axis=1)
        X.columns = ['sma', 'bb', 'momentum']
        return X


    def add_evidence(  		  	   		  	  			  		 			     			  	 
        self,  		  	   		  	  			  		 			     			  	 
        symbol="JPM",
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2009, 12, 31),
        sv=100000,
    ):
        # add your code to do learning here  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        # example usage of the old backward compatible util function  		  	   		  	  			  		 			     			  	 
        syms = [symbol]
        dates = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        #print(prices_all)
        prices = prices_all[syms]  # only portfolio symbols
        #print(prices)
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

        X = self.X_factors(prices, self.day_sma, self.day_bb, self.day_m)
        Y = self.Y_calculator(prices, self.days_y, YSELL=self.YSELL, YBUY=self.YBUY, impact=self.impact)

        #X = X.iloc[:]
        data = X.join(Y)
        data.ffill(inplace=True)
        data.fillna(0, inplace=True)
        data = data.values #convert to ndarray
        newx = data[:, 0:-1]
        newy = data[:, -1]
        learner = bl.BagLearner(rt.RTLearner, bags=self.bags, kwargs={'leaf_size': self.leaf_size}, boost=True, verbose=False)
        trainmodel = learner.add_evidence(newx, newy)
        self.learner = learner
        #bag = learner.add_evidence(X, Y)
        #pred_y = learner.query(X)
        '''
        if self.verbose:  		  	   		  	  			  		 			     			  	 
            print(prices)  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        # example use with new colname  		  	   		  	  			  		 			     			  	 
        volume_all = ut.get_data(  		  	   		  	  			  		 			     			  	 
            syms, dates, colname="Volume"  		  	   		  	  			  		 			     			  	 
        )  # automatically adds SPY  		  	   		  	  			  		 			     			  	 
        volume = volume_all[syms]  # only portfolio symbols  		  	   		  	  			  		 			     			  	 
        volume_SPY = volume_all["SPY"]  # only SPY, for comparison later  		  	   		  	  			  		 			     			  	 
        if self.verbose:  		  	   		  	  			  		 			     			  	 
            print(volume)
        '''

        return trainmodel

    # this method should use the existing policy and test it against new data  		  	   		  	  			  		 			     			  	 
    def testPolicy(  		  	   		  	  			  		 			     			  	 
        self,  		  	   		  	  			  		 			     			  	 
        symbol="JPM",
        sd=dt.datetime(2008, 1, 1),
        ed=dt.datetime(2009, 12, 31),
        sv=100000,
    ):  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        Tests your learner using data outside of the training data  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        :param symbol: The stock symbol that you trained on on  		  	   		  	  			  		 			     			  	 
        :type symbol: str  		  	   		  	  			  		 			     			  	 
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  	  			  		 			     			  	 
        :type sd: datetime  		  	   		  	  			  		 			     			  	 
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  	  			  		 			     			  	 
        :type ed: datetime  		  	   		  	  			  		 			     			  	 
        :param sv: The starting value of the portfolio  		  	   		  	  			  		 			     			  	 
        :type sv: int  		  	   		  	  			  		 			     			  	 
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		  	  			  		 			     			  	 
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		  	  			  		 			     			  	 
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		  	  			  		 			     			  	 
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		  	  			  		 			     			  	 
        :rtype: pandas.DataFrame  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        # here we build a fake set of trades  		  	   		  	  			  		 			     			  	 
        # your code should return the same sort of data  		  	   		  	  			  		 			     			  	 
        dates = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        syms = [symbol]
        prices = prices_all[syms]
        trades = prices_all[[symbol,]]  # only portfolio symbols  		  	   		  	  			  		 			     			  	 
        trades_SPY = prices_all["SPY"]  # only SPY, for comparison later

        X = self.X_factors(prices, self.day_sma, self.day_bb, self.day_m)
        index = X.index[:]

        Y = self.Y_calculator(prices, 10, YSELL=self.YSELL, YBUY=self.YBUY, impact=self.impact)
        data = X.join(Y)
        data.ffill(inplace=True)
        data.fillna(0, inplace=True)
        data = data.values #convert to ndarray
        newx = data[:, 0:-1]
        newy = data[:, -1]

        learner = self.learner
        pred_y = learner.query(newx)


        #holdings = pred_y * 1000
        holdings = pd.DataFrame(np.nan, index=index, columns=['holds'])
        for i in range(pred_y.shape[0]):
            if (pred_y[i] == -1):
                holdings.iloc[i] = -1000
            elif (pred_y[i] == 1):
                holdings.iloc[i] = 1000
            elif (pred_y[i] == 0):
                holdings.iloc[i] = 0
            #else:
                #holdings.iloc[i] = 0
        holdings.ffill(inplace=True)
        holdings.fillna(0, inplace=True)
        trades = holdings.diff()
        if holdings.iloc[0].values == 0:
            trades.iloc[0] = 0
        else:
            trades.iloc[0] = holdings.iloc[0]




        if self.verbose:  		  	   		  	  			  		 			     			  	 
            print(type(trades))  # it better be a DataFrame!  		  	   		  	  			  		 			     			  	 
        if self.verbose:  		  	   		  	  			  		 			     			  	 
            print(trades)  		  	   		  	  			  		 			     			  	 
        if self.verbose:  		  	   		  	  			  		 			     			  	 
            print(prices_all)

        df_trades = pd.DataFrame(data=trades.values, index=trades.index, columns=['Shares'])
        #portval = marketsimcode.compute_portvals(orders=df_trades, start_val=sv, commission=self.commission, impact=self.impact)

        return df_trades

    def author(self):
        return 'twu411'

  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
if __name__ == "__main__":  		  	   		  	  			  		 			     			  	 
    print("One does not simply think up a strategy")  		  	   		  	  			  		 			     			  	 
