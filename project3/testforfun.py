""""""
"""  		  	   		  	  			  		 			     			  	 
Test a learner.  (c) 2015 Tucker Balch  		  	   		  	  			  		 			     			  	 

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
"""

import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import LinRegLearner as lrl
import DTLearner as dt
import BagLearner as bl
import RTLearner as rt
import InsaneLearner as it
import time


def converttype(a):
    # convert the element to floeat, if the element is not convertable, throw error and return 'no'
    try:
        return float(a)
    except ValueError:
        return "no"


sys.argv.append("Data/Istanbul.csv")
if __name__ == "__main__":
    np.random.seed(596568372)
    if len(sys.argv) != 2:
        print("Usage: python testlearner.py <filename>")
        sys.exit(1)
    inf = open(sys.argv[1], "r+")
    rawdata = [list(s.strip().split(",")) for s in inf.readlines()]
    # delete first line if full of strings
    no = []
    no2 = []
    for i in range(len(rawdata[0])):
        no.append('no')
        no2.append(converttype(rawdata[0][i]))
    if no == no2:
        del rawdata[0]
    # moniter datatype of first column, delete the column if it is string
    for l in rawdata:
        for s in l:
            if converttype(s) == "no":
                l.remove(s)
    data = np.array(list(rawdata)).astype(np.float)

    # compute how much of the data is training and testing
    train_rows = int(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    train_x = data[:train_rows, 0:-1]
    train_y = data[:train_rows, -1]
    test_x = data[train_rows:, 0:-1]
    test_y = data[train_rows:, -1]

    print(f"{test_x.shape}")
    print(f"{test_y.shape}")




    dtrmse = []

    for i in range(1, 51):

        # create a learner and train it
        learner = dt.DTLearner(verbose=False, leaf_size=i)  # create a Learner
        learner.add_evidence(train_x, train_y) # train it
        # evaluate in sample
        pred_y = learner.query(train_x)  # get the predictions
        rmse_train = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
        c_train = np.corrcoef(pred_y, y=train_y)
        # evaluate out of sample
        pred_y = learner.query(test_x)  # get the predictions
        rmse_test = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        c_test = np.corrcoef(pred_y, y=test_y)
        dtrmse.append([rmse_train, rmse_test])
    nd_dtrmse = np.array(dtrmse)
    df1 = pd.DataFrame(nd_dtrmse, index=range(1, 51), columns=['training data', 'testing data'])
    #print(df1)

    #plot leaf_size vs rmse in dt cases
    ax = df1.plot(title='Effect of leaf size on dt learner', fontsize=12)
    ax.set_xlabel('Leaf size')
    ax.set_ylabel('Root mean square error')
    plt.savefig('.//images//Figure1.png')
    plt.close()
    #experiment 2 figure
    dtrmse2 = []
    for leaf_size in range(1, 51):
        learner2 = bl.BagLearner(dt.DTLearner, bags=5, kwargs={'leaf_size': leaf_size},boost=True, verbose=False)
        learner2.add_evidence(train_x, train_y)  # train it
        # evaluate in sample
        pred_y = learner2.query(train_x)  # get the predictions
        rmse_train = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
        # evaluate out of sample
        pred_y = learner2.query(test_x)  # get the predictions
        rmse_test = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        dtrmse2.append([rmse_train, rmse_test])
    nd_dtrmse2 = np.array(dtrmse2)
    df2 = pd.DataFrame(nd_dtrmse2, index=range(1, 51), columns=['training data', 'testing data'])
    ax = df2.plot(title='5-bag case on dt learner', fontsize=12)
    ax.set_xlabel('Leaf size')
    ax.set_ylabel('Root mean square error')
    plt.savefig('.//images//Figure2-1.png')
    plt.close()

    dtrmse2 = []
    for leaf_size in range(1, 51):
        learner2 = bl.BagLearner(dt.DTLearner, bags=20, kwargs={'leaf_size': leaf_size}, boost=True, verbose=False)
        learner2.add_evidence(train_x, train_y)  # train it
        # evaluate in sample
        pred_y = learner2.query(train_x)  # get the predictions
        rmse_train = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
        # evaluate out of sample
        pred_y = learner2.query(test_x)  # get the predictions
        rmse_test = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        dtrmse2.append([rmse_train, rmse_test])
    nd_dtrmse2 = np.array(dtrmse2)
    df2 = pd.DataFrame(nd_dtrmse2, index=range(1, 51), columns=['training data', 'testing data'])
    ax = df2.plot(title='20-bag case on dt learner', fontsize=12)
    ax.set_xlabel('Leaf size')
    ax.set_ylabel('Root mean square error')
    plt.savefig('.//images//Figure2-2.png')
    plt.close()

    dtrmse2 = []
    for leaf_size in range(1, 51):
        learner2 = bl.BagLearner(dt.DTLearner, bags=100, kwargs={'leaf_size': leaf_size},boost=True, verbose=False)
        learner2.add_evidence(train_x, train_y)  # train it
        # evaluate in sample
        pred_y = learner2.query(train_x)  # get the predictions
        rmse_train = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
        # evaluate out of sample
        pred_y = learner2.query(test_x)  # get the predictions
        rmse_test = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        dtrmse2.append([rmse_train, rmse_test])
    nd_dtrmse2 = np.array(dtrmse2)
    df2 = pd.DataFrame(nd_dtrmse2, index=range(1, 51), columns=['training data', 'testing data'])
    ax = df2.plot(title='100-bag case on dt learner', fontsize=12)
    ax.set_xlabel('Leaf size')
    ax.set_ylabel('Root mean square error')
    plt.savefig('.//images//Figure2-3.png')
    plt.close()



    timelist = []
    madlist = []
    for leaf_size in range(1, 51):
        t0 = time.time()
        learner3 = dt.DTLearner(leaf_size=leaf_size, verbose=False)
        learner3.add_evidence(train_x, train_y)  # train it
        t1 = time.time()
        t_dttrain = t1 - t0
        dt_pred_y = learner3.query(test_x)
        dt_mad = (np.abs(test_y - dt_pred_y)).mean()

        t2 = time.time()
        learner4 = rt.RTLearner(leaf_size=leaf_size, verbose=False)
        learner4.add_evidence(train_x, train_y)
        t3 = time.time()
        t_rttrain = t3 - t2
        rt_pred_y = learner4.query(test_x)
        rt_mad = (np.abs(test_y - rt_pred_y)).mean()
        #create list to record the time and mad data
        timelist.append([t_dttrain, t_rttrain])
        madlist.append([dt_mad, rt_mad])

    #plot training time figure
    ndtimelist = np.array(timelist)
    df3 = pd.DataFrame(ndtimelist, index=range(1,51), columns=['DT training', 'RT training'])
    ax = df3.plot(title='Comparison of training time between DT and RT', fontsize=12)
    ax.set_xlabel('Leaf size')
    ax.set_ylabel('Training time')
    plt.savefig('.//images//Figure3-1.png')
    plt.close()
    #plot mad figure
    ndmadlist = np.array(madlist)
    df3 = pd.DataFrame(ndmadlist, index=range(1,51), columns=['DT testing', 'RT testing'])
    ax = df3.plot(title='Comparison of MAD between DT and RT', fontsize=12)
    ax.set_xlabel('Leaf size')
    ax.set_ylabel('Mean absolute deviation')
    plt.yticks(np.arange(0.003, 0.007, step=0.001))
    plt.savefig('.//images//Figure3-2.png')
    plt.close()
















