# standard imports
# third party imports
import pysgpp
# application imports
import custom_logger as Log
from pre_processing import PreProcessing

"""
@Author:    Ingo Mayer
Created:    30.05.2017

Changed:    04.06.2017

Description: Provides functions for the main steps in creating a time series prediction
             sparse grid.

"""


class TimeSeriesPipeline(object):
    def __init__(self):
        pass

    # ToDo: experiment with grid types & adaptivity; for now use linear, regular grid
    def create_grid(self, dimension, level):
        self.dimension = dimension
        self.grid = pysgpp.Grid.createLinearGrid(dimension)
        # create a regular sparse grid of specified level
        self.grid.getGenerator().regular(level)
        Log.info(self.__class__.__name__, "Created linear grid with dimension " + str(dimension)
                 + " and level " + str(level))

    def load_training_data(self, file):
        # ToDo: read csv file
        # ToDo: call preprocessing to transform data into the necessary n-dimensional construct
        pass

    def add_training_data(self, timeseries):
        self.training_data = PreProcessing().transform_timeseries_to_datamatrix(timeseries, self.dimension)

    def create_linear_system(self):
        pass

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