import numpy as np
import random
from scipy import stats
class RTLearner(object):
    """
    This is a DTLearner. It is implemented correctly.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool
    """

    def __init__(self, leaf_size = 1, verbose=False):
        """
        Constructor method
        """
        self.leaf_size = leaf_size
        self.verbose = verbose
        pass  # move along, these aren't the drones you're looking for

    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "twu411"  # replace tb34 with your Georgia Tech username
    def optfactor(self, data_x, data_y):
        #random.seed(596568372)
        i = random.randint(0, data_x.shape[1]-1)

        return i

    def build_tree(self, data):
        #termination condition: leaf size limitation or all y are equal
        if data.shape[0] <= self.leaf_size or np.std(data[:, -1]) == 0:
            c = np.empty((data.shape[0], 4))
            c[:, 0] = -1
            c[:, 1] = stats.mode(data[:, -1])[0][0]
            c[:, 2:] = -100
            return c

        facter = self.optfactor(data[:, 0:-1], data[:, -1])
        splitval = np.median(data[:, facter])
        #judge if median could not divide tree any more
        if np.all(data[:, facter] <= splitval):
            c = np.array([[-1, stats.mode(data[:, -1])[0][0], -100, -100]])
            return c

        #recursion starts here:
        lefttree = self.build_tree(data[data[:, facter] <= splitval])
        righttree = self.build_tree(data[data[:, facter] > splitval])
        root = np.array(([facter, splitval, 1, lefttree.shape[0] + 1],))
        c = np.concatenate((root, lefttree, righttree), axis=0)
        return c

    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """

        # combine x and y to be introduced into trees
        new_y = np.array(data_y, copy=False, subok=True, ndmin=2).T
        data = np.column_stack([data_x, data_y]) #column stack is used because concatenate or append somehow doesn't work
        self.tree = self.build_tree(data)
        if self.verbose == True:
            print("tree:\n", self.build_tree(data))
            print("tree shape:\n", self.build_tree(data).shape)


        # build and save the model

    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        tree = self.tree

        testy = np.array(())
        for test in points:
            treenode = 0
            while int(tree[treenode, 0]) != -1:
                facter = int(tree[treenode, 0])

                if test[facter] <= tree[treenode, 1]:
                    treenode = treenode + int(tree[treenode, 2])
                else:
                    treenode = treenode + int(tree[treenode, 3])
            # I have to write the following three-line shit because we are not allowed to use lists.
            thisy = tree[treenode, 1]
            thisy = np.array((thisy))
            testy = np.append(testy, thisy)
        return testy

if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")

