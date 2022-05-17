""""""  		  	   		  	  			  		 			     			  	 
"""  		  	   		  	  			  		 			     			  	 
template for generating data to fool learners (c) 2016 Tucker Balch  		  	   		  	  			  		 			     			  	 
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
  		  	   		  	  			  		 			     			  	 
import math  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
import numpy as np
import random
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
# this function should return a dataset (X and Y) that will work  		  	   		  	  			  		 			     			  	 
# better for linear regression than decision trees  		  	   		  	  			  		 			     			  	 
def best_4_lin_reg(seed=596568372):
    """  		  	   		  	  			  		 			     			  	 
    Returns data that performs significantly better with LinRegLearner than DTLearner.  		  	   		  	  			  		 			     			  	 
    The data set should include from 2 to 10 columns in X, and one column in Y.  		  	   		  	  			  		 			     			  	 
    The data should contain from 10 (minimum) to 1000 (maximum) rows.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    :param seed: The random seed for your data generation.  		  	   		  	  			  		 			     			  	 
    :type seed: int  		  	   		  	  			  		 			     			  	 
    :return: Returns data that performs significantly better with LinRegLearner than DTLearner.  		  	   		  	  			  		 			     			  	 
    :rtype: numpy.ndarray  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    np.random.seed(seed)
    col_num = np.random.randint(2,11)
    row_num = np.random.randint(100, 1001)
    a = (np.random.random(col_num) - 0.5) * 20
    b = (np.random.random() - 0.5) * 20
    x = np.random.random((row_num, col_num)) * 100
    y = np.dot(x, a) + b + (np.random.randn(row_num))
    # Here's is an example of creating a Y from randomly generated  		  	   		  	  			  		 			     			  	 
    # X with multiple columns  		  	   		  	  			  		 			     			  	 
    # y = x[:,0] + np.sin(x[:,1]) + x[:,2]**2 + x[:,3]**3
    return x, y  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
def best_4_dt(seed=596568372):
    """  		  	   		  	  			  		 			     			  	 
    Returns data that performs significantly better with DTLearner than LinRegLearner.  		  	   		  	  			  		 			     			  	 
    The data set should include from 2 to 10 columns in X, and one column in Y.  		  	   		  	  			  		 			     			  	 
    The data should contain from 10 (minimum) to 1000 (maximum) rows.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    :param seed: The random seed for your data generation.  		  	   		  	  			  		 			     			  	 
    :type seed: int  		  	   		  	  			  		 			     			  	 
    :return: Returns data that performs significantly better with DTLearner than LinRegLearner.  		  	   		  	  			  		 			     			  	 
    :rtype: numpy.ndarray  		  	   		  	  			  		 			     			  	 
    """
    np.random.seed(seed)
    col_num = np.random.randint(2,11)
    row_num = np.random.randint(100, 1001)
    class_num = np.random.randint(10, 15)
    x = np.random.random((row_num, col_num))
    y = np.maximum(x[:, 0], x[:, 1])
    for i in range(col_num):
        y = y * np.sin(x[:, i]) ** i

    return x, y


    """
    np.random.seed(seed)
    col_num = np.random.randint(2,11)
    row_num = np.random.randint(100, 1001)
    class_num = np.random.randint(10, 15)
    x = np.random.random((row_num, col_num))
    y = np.zeros(row_num)
    indexlist = list(range(0, row_num))
    center = []


    for i in range(class_num):
        center.append(np.random.random(col_num)) # ai: a center point
        
    while len(indexlist) != 0:
        thisindex = random.choice(indexlist) # thisindex: number being chosen to be assigned a point nearby the center
        currentindex = indexlist.index(thisindex) #currentindex: index of the number above
        indexlist.pop(currentindex)
        a = random.randint(0, len(center) - 1)
        currentcenter = center[a]
        x[thisindex, :] = currentcenter * 100 + np.random.random((1, col_num))
        y[thisindex] = a * 10 + random.random()
    return x, y
    """



  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
def author():  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    :return: The GT username of the student  		  	   		  	  			  		 			     			  	 
    :rtype: str  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    return "twu411"  # Change this to your user ID
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
if __name__ == "__main__":  		  	   		  	  			  		 			     			  	 
    print("they call me Tim.")

