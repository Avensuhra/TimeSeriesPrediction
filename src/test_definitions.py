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

Changed:    04.06.2017

Description: Defines tests for non-csv file based tests like the Henon map, where the time series
             is calculated from a function.

"""

class HenonTest(object):
    _timeseries = None
    _pipeline = None

    def __init__(self, level, total_length, training_length, lambda_parameter, a, b, x_0, x_1):
        self._timeseries = self._calculate_timeseries(total_length, a, b, x_0, x_1)
        self._create_pipeline(2, level, self._timeseries[:(training_length + 2)], lambda_parameter)

    def _calculate_timeseries(self, length, a, b, x_0, x_1):
        values = []
        values.append(x_0)
        values.append(x_1)
        for i in xrange(2, length):
            values.append(a - pow(values[i - 1], 2) + b*values[i - 2])
        return values

    def _create_pipeline(self, dimension, level, training_series, lambda_parameter):
        training_data = PreProcessing().transform_timeseries_to_datatuple(training_series, dimension)
        self._pipeline = TimeSeriesPipeline()
        self._pipeline.create_learner_with_reshaped_data(level, lambda_parameter, training_data)
        self._pipeline.get_training_error(training_data)





