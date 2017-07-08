# standard imports
import numpy as np
# third party imports
import matplotlib.pyplot as plt
import pysgpp
# application imports
import logging as Log
from pre_processing import PreProcessing
from file_parser import FileParser
from pysgpp.extensions.datadriven.learner import LearnerBuilder
from pysgpp.extensions.datadriven.controller.InfoToFile import InfoToScreen
from pysgpp.extensions.datadriven.learner import SolverTypes
from pysgpp import DataVector
from timeseries_learner import TimeseriesLearner

"""
@Author:    Ingo Mayer
Created:    30.05.2017

Changed:    07.07.2017

Description: Provides functions for the main steps in creating a time series prediction
             sparse grid.

"""


def f(x):
    return np.prod(4. * x * (1 - x), axis=1)

# ToDo: Check out LearnerBuilder - possibly the steps done so far are included in that already

class TimeSeriesPipeline(object):
    def __init__(self):
        self._learner = None
        self._testing_data = None

    # ToDo: experiment with grid types & adaptivity; for now use linear, regular grid
    def create_learner_with_file(self, level, lambda_parameter, file_name):
        training_data = FileParser().arff_to_numpy(file_name)
        self._create_learner(level, PreProcessing().scale_to_correct_interval(training_data[0]),
                             PreProcessing().scale_to_correct_interval(training_data[1]), lambda_parameter)

    def create_learner_with_array(self, level, lambda_parameter, data):
        self._create_learner(level, PreProcessing().scale_to_correct_interval(data[0]),
                             PreProcessing().scale_to_correct_interval(data[1]), lambda_parameter)

    def create_learner_with_reshaped_data(self, level, lambda_parameter, data):
        Log.debug("Creating regression with lambda " + str(lambda_parameter) + " and level " + str(level))
        self._create_learner(level, data[0], data[1], lambda_parameter)

    def _create_learner(self, level, scaled_samples, scaled_values, lambda_parameter):
        self._learner = TimeseriesLearner()
        self._learner.set_training_data(scaled_samples, scaled_values)
        self._learner.set_grid(level)
        self._learner.set_specification(lambda_parameter)
        self._learner.set_stop_policy()
        self._learner.set_solver(SolverTypes.CG)
        self._learner.get_result()

    def set_testing_data_with_file(self, file_name):
        if self._learner is not None:
            data = FileParser().arff_to_numpy(file_name)
            self._set_testing_data(PreProcessing().scale_to_correct_interval(data[0]),
                                   PreProcessing().scale_to_correct_interval(data[1]))
        else:
            Log.error("Need to set learner before specifying testing data.")

    def set_testing_data_with_array(self, data):
        if self._learner is not None:
            self._set_testing_data(PreProcessing().scale_to_correct_interval(data[0]),
                                   PreProcessing().scale_to_correct_interval(data[1]))
        else:
            Log.error("Need to set learner before specifying testing data.")

    def _set_testing_data(self, samples, values):
        self._testing_data = []
        self._testing_data.append(samples)
        self._testing_data.append(values)

    # ToDo: Possibly move this to a separate solver class
    def precondition_solver(self):
        pass

    def test_regression(self, n):
        if self._learner is not None and self._testing_data is not None:
            pass
        else:
            Log.error("Need to set learner before specifying testing data.")

    # ToDo: Move this to a separate post-proecessing or evaluation class
    def compare_prediction(self, ground_truth):
        pass

    def get_training_error(self, training_data):
        truth_vector = training_data[1]
        sample_array = training_data[0]
        prediction_vector = []
        for i in xrange(len(sample_array)):
            prediction_vector.append(self._learner.predict_next_value(sample_array[i]))
        return self.calculate_mean_error(prediction_vector, truth_vector)

    def calculate_mean_error(self, prediction_vector, actual_vector):
        sum = 0
        for i in range(len(prediction_vector)):
            sum += pow((prediction_vector[i] - actual_vector[i]), 2)

        return np.sqrt(sum/len(prediction_vector))



