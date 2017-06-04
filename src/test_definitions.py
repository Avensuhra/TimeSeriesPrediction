# standard imports
# third party imports
import pysgpp
# application imports
import custom_logger as Log
from timeseries_pipeline import TimeSeriesPipeline

"""
@Author:    Ingo Mayer
Created:    04.06.2017

Changed:    04.06.2017

Description: Defines tests for non-csv file based tests like the Henon map, where the time series
             is calculated from a function.

"""

class HenonTest(object):
    def __init__(self, level, total_length, training_length, a, b, x_0, x_1):
        self._timeseries = self._calculate_timeseries(total_length, a, b, x_0, x_1)
        self._create_pipeline(2, level, self._timeseries[:training_length])

    def _calculate_timeseries(self, length, a, b, x_0, x_1):
        values = []
        values.append(x_0)
        values.append(x_1)
        for i in xrange(2, length):
            values.append(a - pow(values[i - 1], 2) + b*values[i - 2])
        return values

    def _create_pipeline(self, dimension, level, training_series):
        pipeline = TimeSeriesPipeline()
        pipeline.create_grid(dimension, level)
        pipeline.add_training_data(training_series)



