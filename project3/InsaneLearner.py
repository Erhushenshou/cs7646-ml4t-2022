import numpy as np
import BagLearner as bl
import LinRegLearner as lrl
class InsaneLearner(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.learnerlist = []
        for i in range(20):
            self.learnerlist.append(bl.BagLearner(learner=lrl.LinRegLearner, kwargs={},  bags=20, boost=False, verbose=self.verbose))
    def author(self):
        return("twu411")
    def add_evidence(self, data_x, data_y):
        for i in self.learnerlist:
            i.add_evidence(data_x, data_y)
    def query(self, points):
        Y = np.empty((points.shape[0], 1))
        for i in self.learnerlist:
            Y = np.append(Y, np.array([i.query(points)]).T, axis=1)
        Y_del = np.delete(Y, 0, 1)
        return Y_del.mean(axis=1)


