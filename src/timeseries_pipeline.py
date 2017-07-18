# standard imports
import numpy as np
# third party imports
import matplotlib.pyplot as plt
# application imports
from pysgpp.extensions.datadriven.learner import SolverTypes
from timeseries_learner import TimeseriesLearner
from visualization import Visualization

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

    def create_learner(self, level, scaled_samples, scaled_values, lambda_parameter):
        self._learner = TimeseriesLearner()
        self._learner.set_training_data(scaled_samples, scaled_values)
        self._learner.set_grid(level)
        self._learner.set_specification(lambda_parameter)
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

    def calculate_mean_error(self, prediction_vector, actual_vector):
        sum = 0
        for i in range(len(prediction_vector)):
            sum += pow((prediction_vector[i] - actual_vector[i]), 2)
        #plt.plot(prediction_vector, 'r--', actual_vector, 'g--')
        #plt.show()
        return np.sqrt(sum/len(prediction_vector))



