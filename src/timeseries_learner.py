# standard imports
import logging as Log
import numpy as np
# third party imports
import pysgpp
from pysgpp.extensions.datadriven.learner import LearnerBuilder
from pysgpp import DataVector
from pysgpp.extensions.datadriven.learner import SolverTypes
from pysgpp.extensions.datadriven.controller.InfoToFile import InfoToScreen

# application imports

class TimeseriesLearner(object):
    def __init__(self):
        self._builder = LearnerBuilder().buildRegressor()
        self._learner = None

    def set_training_data(self, scaled_samples, scaled_values):
        self._builder = self._builder.withTrainingDataFromNumPyArray(scaled_samples, scaled_values)

    def set_grid(self, level):
        self._builder = self._builder.withGrid().withLevel(level)

    def set_specification(self, lambda_parameter):
        self._builder = self._builder.withSpecification().withLambda(lambda_parameter)

    def set_stop_policy(self):
        self._builder = self._builder.withStopPolicy()

    def set_solver(self, type):
        if type == SolverTypes.CG:
            self._builder = self._builder.withCGSolver()

    def get_result(self):
        self._learner = self._builder.withProgressPresenter(InfoToScreen()).andGetResult()
        gs = self._learner.grid.getStorage()
        Log.debug("Grid points: %i" % gs.getSize())
        self._learner.learnData()

    def predict_next_value(self, test_vector):
        opEval = pysgpp.createOperationEval(self._learner.grid)
        vector = DataVector(len(test_vector))
        for i in xrange(len(test_vector)):
            vector[i] = test_vector[i]
        return opEval.eval(self._learner.alpha, vector)