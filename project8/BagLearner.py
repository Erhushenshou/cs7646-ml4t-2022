import numpy as np
import random
from scipy import stats

class BagLearner(object):
    """
    This is a DTLearner. It is implemented correctly.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool
    """

    def __init__(self, learner, kwargs, bags = 10, boost = True, verbose = True):
        """
        Constructor method
        """

        self.verbose = verbose
        self.boost = boost
        self.bags = bags
        self.learner = learner
        self.kwargs = kwargs
        self.baglist = []


    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "twu411"  # replace tb34 with your Georgia Tech username

    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        data = np.column_stack([data_x, data_y]) #column stack is used because concatenate or append somehow doesn't work

        learnersaver = []
        #generate bags:
        for i in range(0, self.bags):
            thislearner = self.learner(**self.kwargs)
            thisindex = self.genindex(data)
            bagx = data_x[thisindex]
            bagy = data_y[thisindex]
            thislearner.add_evidence(bagx, bagy) # call the add evidence function in their own class, not this class
            self.baglist.append(thislearner)

        if self.verbose == True:
            print("bag number:\n", self.bags)
        return self.baglist


    def genindex(self, data):
        #random.seed(596568372)
        self.data = data
        indexlist = []
        bag_rows = int(data.shape[0])
        for i in range (0, bag_rows):
            indexlist.append(random.randint(0, data.shape[0] - 1))
        return indexlist

    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        Y = np.empty((points.shape[0], 1))
        for i in self.baglist:
            Y = np.append(Y, np.array([i.query(points)]).T, axis=1)
        Y_del = np.delete(Y, 0, 1)
        pred_y = stats.mode(Y_del.transpose())[0][0]
        return pred_y


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")

