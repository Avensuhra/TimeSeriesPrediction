# standard imports
import logging as Log
# third party imports
import pysgpp
from pysgpp.extensions.datadriven.learner import LearnerBuilder, SolverTypes
from pysgpp import DataVector
from pysgpp.extensions.datadriven.controller.InfoToFile import InfoToScreen
from pysgpp.extensions.datadriven.learner import Types
# application imports

class TimeseriesLearner(object):
    def __init__(self):
        self._builder = LearnerBuilder().buildRegressor()
        self._learner = None

    def set_training_data(self, scaled_samples, scaled_values):
        self._builder = self._builder.withTrainingDataFromNumPyArray(scaled_samples, scaled_values)

    def set_grid(self, level):
        self._builder = self._builder.withGrid().withLevel(level).withBorder(Types.BorderTypes.NONE)

    def set_specification(self, lambda_parameter, with_adaptivity, rate, threshold):
        if(with_adaptivity):
            self._builder = self._builder.withSpecification().withLambda(lambda_parameter).withAdaptRate(rate).withAdaptThreshold(threshold)
        else:
            self._builder = self._builder.withSpecification().withLambda(lambda_parameter)

    def set_folding_policy(self):
        self._builder.withRandomFoldingPolicy().withLevel(3)

    def set_stop_policy(self):
        self._builder = self._builder.withStopPolicy().withAdaptiveItarationLimit(5)

    def set_solver(self, type, accuracy):
        if type == SolverTypes.CG:
            self._builder = self._builder.withCGSolver().withAccuracy(accuracy).withImax(400)

    def get_result(self):   
        self._learner = self._builder.andGetResult()#.withProgressPresenter(InfoToScreen())
        gs = self._learner.grid.getStorage()
        alpha = DataVector(gs.getSize(), 0.0)
        self._learner.errors = alpha
        self._learner.refineGrid()
        self._learner.learnData()

    def retrain(self):
        self._learner.learnData()

    def predict_next_value(self, test_vector):
        opEval = pysgpp.createOperationEval(self._learner.grid)
        vector = DataVector(len(test_vector))
        for i in xrange(len(test_vector)):
            vector[i] = test_vector[i]
        return opEval.eval(self._learner.alpha, vector)


