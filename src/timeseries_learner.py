# standard imports
import logging as Log
import numpy as np
# third party imports
import pysgpp
from pysgpp.extensions.datadriven.learner import LearnerBuilder, Learner, TrainingStopPolicy, TrainingSpecification, SolverTypes
from pysgpp import DataVector, Grid, ConjugateGradients, DataMatrix
from pysgpp.extensions.datadriven.controller import LearnerEventController
from pysgpp.extensions.datadriven.controller.InfoToFile import InfoToScreen
from pysgpp.extensions.datadriven.data import DataContainer
from pysgpp import (createOperationLaplace,
                    createOperationIdentity)

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

    def set_folding_policy(self):
        self._builder.withRandomFoldingPolicy().withLevel(3)

    def set_stop_policy(self):
        self._builder = self._builder.withStopPolicy()

    def set_solver(self, type, accuracy):
        if type == SolverTypes.CG:
            self._builder = self._builder.withCGSolver().withAccuracy(accuracy).withImax(1000)

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


class CustomLearner(object):
    _learner = None
    _observer = None
    _dimension = 0

    def __init__(self, dimension, level, regression_parameter):
        self._dimension = dimension
        self._learner = Learner()
        grid = Grid.createLinearGrid(dimension)
        grid.getGenerator().regular(level)
        self._learner.setGrid(grid)
        # ToDo: What's epsilon?
        solver = ConjugateGradients(1000, regression_parameter)
        self._learner.setSolver(solver)
        stop_policy = TrainingStopPolicy()
        stop_policy.setAccuracyLimit(pow(1.03*10, -4))
        self._learner.setStopPolicy(stop_policy)
        specification = TrainingSpecification()
        specification.setL(regression_parameter)
        specification.setCOperator(createOperationIdentity(grid))
        self._learner.setSpecification(specification)

    def set_training_data(self, points, values):
        size = len(points)
        dataMatrix = DataMatrix(size, self._dimension)
        tempVector = DataVector(self._dimension)
        valuesVector = DataVector(size)
        for rowIndex in xrange(size):
            for colIndex in xrange(self._dimension):
                tempVector[colIndex] = points[rowIndex][colIndex]
            dataMatrix.setRow(rowIndex, tempVector)
            valuesVector[rowIndex] = values[rowIndex]
        # ToDo: Figure out how the datacontainer has to be structured, python documentation somewhat unclear
        data = DataContainer(points=dataMatrix, values=valuesVector)
        self._learner.setDataContainer(data)
        #data = DataContainer()
        #data.points = points
        #data.values = values
        #self._learner.setDataContainer(data)

    def learn(self):
        if self._learner.dataContainer is not None:
            self._learner.learnData()



