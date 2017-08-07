# standard imports
import numpy as np
# third party imports
import matplotlib.pyplot as plt
# application imports
from pysgpp.extensions.datadriven.learner import SolverTypes
from pipeline.sparsegrid.timeseries_learner import TimeseriesLearner
from view.visualization import Visualization

"""
@Author:    Ingo Mayer
Created:    30.05.2017

Changed:    07.07.2017

Description: Provides functions for the main steps in creating a time series prediction
             sparse grid.

"""


class TimeSeriesPipeline(object):
    def __init__(self, training_accuracy):
        self._learner = None
        self._testing_data = None
        self._accuracy = training_accuracy

    def create_learner(self, level, scaled_samples, scaled_values, lambda_parameter, with_adaptivity):
        self._learner = TimeseriesLearner()
        self._learner.set_training_data(scaled_samples, scaled_values)
        self._learner.set_grid(level)
        self._learner.set_specification(lambda_parameter, with_adaptivity)
        self._learner.set_stop_policy()
        self._learner.set_solver(SolverTypes.CG, self._accuracy)
        self._learner.get_result()

    # ToDo: Possibly move this to a separate solver class, cgsolver already preconditions itself with identity matrix
    def precondition_solver(self):
        pass

    def get_prediction_error(self, samples, values):
        prediction_vector = []
        for i in xrange(len(samples)):
            prediction_vector.append(self._learner.predict_next_value(samples[i]))
        return self.calculate_mean_error(prediction_vector, values)

    # Predicts n values for each delay vector
    def predict_n_values(self, samples, n):
        next_values_matrix = []
        for i in xrange(len(samples)):
            next_values_matrix.append([])
            sample_vector = samples[i]
            for j in xrange(n):
                next_value = self._learner.predict_next_value(sample_vector)
                sample_vector = sample_vector[1:]
                sample_vector.append(next_value)
                next_values_matrix[i][j] = next_value
        return next_values_matrix

    # Predicts n values for each delay vector, then calculates overall prediction error
    def predict_n_values_with_error_calc(self, samples, values, n):
        matrix = self.predict_n_values(samples, n)
        # ToDO: Do overall error calculatiion
        #start with i = 0
        # for each i in xrange(len(samples))
        #   take value range[i:n + i] - compare prediction vector[i] to value[i]
        #   calculate difference between actual value and prediction
        # loop moves value range 1 forward
        #
        # loop over differences, square them and sum up
        # divide by number of elements in difference vector (has to be n*len(samples)
        # take square root

    def calculate_mean_error(self, prediction_vector, actual_vector):
        sum = 0
        for i in range(len(prediction_vector)):
            sum += pow((prediction_vector[i] - actual_vector[i]), 2)
        plt.plot(prediction_vector, 'ro', actual_vector, 'g--')
        plt.show()
        return np.sqrt(sum/len(prediction_vector))



