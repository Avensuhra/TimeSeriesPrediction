# standard imports
# third party imports
import pysgpp
# application imports
import custom_logger as Log

"""
@Author:    Ingo Mayer
Created:    30.05.2017

Changed:    04.06.2017


Description: Provides pre-processing functionality for the timeseries pipeline, such as
             transforming a time series into the proper dimensional data.
"""


class PreProcessing(object):
    def __init__(self):
        pass

    # Expects a 1-dimensional numpy array with the earliest value at index 0
    def transform_timeseries_to_datamatrix(self, timeseries, dimension):
        # starts at earliest timestep, each row goes 1 step forward in time
        matrix = pysgpp.DataMatrix(len(timeseries) - 1, dimension)
        for i in xrange(0, matrix.getNrows()):
            for j in xrange(0, dimension):
                # each "dimension" goes 1 step forward in time
                matrix.set(i, j, timeseries[i + j])

        Log.info(self.__class__.__name__, "Created data matrix grid with dimension " + str(dimension)
                 + " and number of rows " + str(len(timeseries)))
        return matrix
