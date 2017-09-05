# standard imports
import logging as Log
# third party imports
import numpy
# application imports

"""
@Author:    Ingo Mayer
Created:    30.05.2017

Changed:    04.06.2017


Description: Provides pre-processing functionality for the timeseries pipeline, such as
             transforming a time series into the proper dimensional data.
"""


class PreProcessing(object):
    scaling_factor = 0

    def __init__(self):
        pass

    # Expects a 1-dimensional numpy array with the earliest value at index 0
    def transform_timeseries_to_datatuple(self, timeseries, dimension):
        # starts at earliest timestep, each row goes 1 step forward in time
        rescaled_series = self.scale_to_correct_interval(timeseries)
        length = len(timeseries) - dimension
        sample_array = numpy.ndarray(shape=(length, dimension))
        for i in xrange(length):
            for j in xrange(dimension):
                # each "dimension" goes 1 step forward in time
                sample_array[i][j] = rescaled_series[i + j]
        value_array = rescaled_series[dimension:]

        return (sample_array, value_array)

    def scale_to_correct_interval(self, timeseries):
        max_value = numpy.amax(timeseries)
        min_value = numpy.amin(timeseries)
        padding = (max_value - min_value)/4
        #print("Min = {0}| Max = {1}| Padding = {2}".format(min_value, max_value, padding))
        max_value += padding
        min_value -= padding
        # rescale
        old_range = max_value - min_value
        new_range = 1 #(1 - 0)
        rescaled_series = []
        for value in timeseries:
            new_value = (((value - min_value)*new_range)/old_range)
            rescaled_series.append(new_value)
        return rescaled_series
