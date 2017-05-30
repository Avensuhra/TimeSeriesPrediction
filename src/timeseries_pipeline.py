import pysgpp

"""
@Author:    Ingo Mayer
Date:       30.05.2017

Description: Provides functions for the main steps in creating a time series prediction
             sparse grid.

"""


class TimeSeriesPipeline(object):
    def __init__(self):
        pass

    def creat_grid(self, dimension, level, gridtype):
        pass

    def define_training_data(self, trainingdata):
        # ToDo: call preprocessing to transform data into the necessary n-dimensional construct
        pass

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

    def predict_next_n_values(self):
        pass

    # ToDo: Move this to a separate post-proecessing or evaluation class
    def compare_prediction(self, ground_truth):
        pass