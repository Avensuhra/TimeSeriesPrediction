# standard imports
# third party imports
import pysgpp
# application imports
import logging as Log
from timeseries_pipeline import TimeSeriesPipeline
from pre_processing import PreProcessing

"""
@Author:    Ingo Mayer
Created:    04.06.2017

Changed:    07.07.2017

Description: Defines tests for non-csv file based tests like the Henon map, where the time series
             is calculated from a function.

"""

class HenonTest(object):
    _timeseries = None
    _pipeline = None
    _training_data = None

    def __init__(self, level, total_length, training_length, lambda_parameter, training_accuracy, a, b, x_0, x_1):
        print("Testing Henon map with parameters: \na = " + str(a) + "\nb = " + str(b))
        print("Lambda: " + str(lambda_parameter))
        print("Grid level: " + str(level))
        print("Total datapoints: " + str(total_length))
        print("Training datapoints: " + str(training_length))
        print("------------------------------------------------------------")
        self._timeseries = self.calculate_timeseries(total_length, a, b, x_0, x_1)
        print("Calculated Henon map values")
        print("------------------------------------------------------------")
        print("Starting training")
        self._create_pipeline(2, level, self._timeseries[:(training_length + 2)], lambda_parameter, training_accuracy)
        print("Finished training")
        print("------------------------------------------------------------")
        print("Starting evaluation of training data")
        print("Testing " + str(len(self._training_data[0])) + " values.")
        print("RMSE Train = " + str(self._pipeline.get_training_error(self._training_data)))
        print("------------------------------------------------------------")
        print("Starting evaluation of testing data")
        test_data = PreProcessing().transform_timeseries_to_datatuple(self._timeseries[(training_length - 2):], 2)
        print("Testing " + str(len(test_data[0])) + " values.")
        print("RMSE Test = " + str(self._pipeline.get_training_error(test_data)))


    def calculate_timeseries(self, length, a, b, x_0, x_1):
        values = []
        values.append(x_0)
        values.append(x_1)
        for i in xrange(2, length):
            values.append(a - pow(values[i - 1], 2) + b*values[i - 2])
        return values

    def _create_pipeline(self, dimension, level, training_series, lambda_parameter, training_accuracy):
        self._training_data = PreProcessing().transform_timeseries_to_datatuple(training_series, dimension)
        self._pipeline = TimeSeriesPipeline(training_accuracy)
        self._pipeline.create_learner_with_reshaped_data(level, lambda_parameter, self._training_data)



class JumpMapTest(object):
    pass


class ForecastingCompetitionTest(object):
    pass


class FinancialDataTest(object):
    pass