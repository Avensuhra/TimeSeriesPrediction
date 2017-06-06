# standard imports
import random
import numpy as np
# third party imports
import matplotlib.pyplot as plt
import pysgpp
# application imports
import custom_logger as Log
from pre_processing import PreProcessing
from file_parser import FileParser
from pysgpp.extensions.datadriven.learner import LearnerBuilder
from pysgpp.extensions.datadriven.controller.InfoToFile import InfoToScreen, InfoToFile
from pysgpp.extensions.datadriven.data.ARFFAdapter import ARFFAdapter
from pysgpp import DataVector
from pysgpp.extensions.datadriven.uq.plot.plot1d import plotSG1d
from pysgpp.extensions.datadriven.uq.plot.plot2d import plotSG2d

"""
@Author:    Ingo Mayer
Created:    30.05.2017

Changed:    04.06.2017

Description: Provides functions for the main steps in creating a time series prediction
             sparse grid.

"""


def f(x):
    return np.prod(4. * x * (1 - x), axis=1)

# ToDo: Check out LearnerBuilder - possibly the steps done so far are included in that already

class TimeSeriesPipeline(object):

    # ToDo: experiment with grid types & adaptivity; for now use linear, regular grid
    def create_grid(self, dimension, level):
        self._dimension = dimension
        self._grid = pysgpp.Grid.createLinearGrid(dimension)
        # create a regular sparse grid of specified level
        self._grid.getGenerator().regular(level)
        Log.info(self.__class__.__name__, "Created linear grid with dimension " + str(dimension)
                 + " and level " + str(level))

    def load_training_data(self, file):
        # ToDo: read csv file
        # ToDo: call preprocessing to transform data into the necessary n-dimensional construct
        pass

    def add_training_data(self, timeseries):
        self._training_data = PreProcessing().transform_timeseries_to_datamatrix(timeseries, self._dimension)

    def create_linear_system(self):
        pass
        # ToDo: Calulate formula 17 of time series paper and stuff into matrix


    # ToDo: Possibly move this to a separate solver class
    def precondition_solver(self):
        pass

    # This will return the alphas
    def solve_linear_system(self):
        pass

    def predict_next_value(self):
        pass

    def predict_next_n_values(self, n):
        pass

    # ToDo: Move this to a separate post-proecessing or evaluation class
    def compare_prediction(self, ground_truth):
        pass

    def learner_builder_test(self):

        """
        file_content = FileParser().arff_to_numpy("../TimeSeriesPrediction/datasets/bank_rejections/bank8FM_train.arff")
        samples = file_content[0]
        values = file_content[1]
        """
        numSamples = 100
        numDims = 2
        samples = np.random.rand(numSamples, numDims)
        values = f(samples)


        print(len(samples), len(values))
        print(samples[0].shape)
        print(values)
        print(samples)

        builder = LearnerBuilder()
        learner = builder.buildRegressor() \
                            .withTrainingDataFromARFFFile("../TimeSeriesPrediction/datasets/bank_rejections/bank8FM_train.arff") \
                            .withTestingDataFromARFFFile("../TimeSeriesPrediction/datasets/bank_rejections/bank8FM_test.arff") \
                            .withGrid().withLevel(2)\
                            .withSpecification().withLambda(pow(2, -17)) \
                            .withStopPolicy()\
                            .withCGSolver()\
                            .withProgressPresenter(InfoToScreen())\
                            .andGetResult()

        # .withTrainingDataFromNumPyArray(samples, values)\

        gs = learner.grid.getStorage()
        print "Dimensions: %i" % gs.getDimension()
        print "Grid points: %i" % gs.getSize()
        learner.learnData()

