# standard imports
from enum import Enum
import math
# third party imports
import nolds
# application imports
from pipeline.timeseries_pipeline import TimeSeriesPipeline
from pipeline.pre_processing import PreProcessing
from finance_data import QuandlDataRetriever, FinanceData

"""
@Author:    Ingo Mayer
Created:    04.06.2017

Changed:    07.07.2017

Description: Defines tests for non-csv file based tests like the Henon map, where the time series
             is calculated from a function.

"""

class TestTypes(Enum):
    HENON = 0,
    JUMP_MAP = 1,
    ANN_COMPETITION = 2,
    FINANCIAL_DATA = 3


class TimeseriesTest(object):
    _timeseries = None
    _scaled_series = None
    _pipeline = None
    _training_length = None
    _with_adaptivity = None

    def __init__(self, type, dimension, level, training_length, lambda_parameter, training_accuracy, quandl_query = "",
                 with_adaptivity=True, testing_length=0):
        print("General Parameters: ")
        print("Lambda: " + str(lambda_parameter))
        print("Grid level: " + str(level))
        print("Training datapoints: " + str(training_length))
        self._training_length = training_length
        self._with_adaptivity = with_adaptivity
        print("------------------------------------------------------------")
        if(type == TestTypes.HENON):
            self._timeseries = self._calculate_henonmap(20000, a=1.4, b=0.3, x_0=0.1, x_1=0.2)
        elif(type == TestTypes.JUMP_MAP):
            self._timeseries = self._calculate_jumpmap(20000, 0.1, 0.2)
        elif(type == TestTypes.ANN_COMPETITION):
            raise NotImplementedError("Ann Competition not implented yet.")
        elif (type == TestTypes.FINANCIAL_DATA):
            self._timeseries = self._finance_test(quandl_query)
            print("Number of chart points: " + str(len(self._timeseries)))
            # ToDo: Decide which chart source to use (e.g. closed, open, etc..) or all of them? Currently: Adjusted Close
        print("------------------------------------------------------------")
        print("Calculating embedding dimension")
        embedding_dims = []
        for i in xrange(1, 101):
            embedding_dims.append(nolds.corr_dim(self._timeseries[:training_length], i))
        max_dim = max(embedding_dims)
        # round for 2 digits accuracy
        if(100*max_dim%100 < 50):
            embedding_dimension = int(math.floor(max_dim))
        else:
            embedding_dimension = int(math.ceil(max_dim))
        print("Embedding dimension: " + str(embedding_dimension))
        # See Takens theorem
        dimension = embedding_dimension*2 + 1
        print("------------------------------------------------------------")
        print("Starting training")
        self._create_pipeline(dimension, level, lambda_parameter, training_accuracy)
        print("Finished training")
        print("------------------------------------------------------------")
        print("Starting evaluation of training data. Predicting 1 step forward for each delay-vector.")
        print("Testing " + str(len(self._scaled_series[0][:training_length])) + " values.")
        print("RMSE Train = " + str(self._pipeline.get_prediction_error(self._scaled_series[0][:training_length], self._scaled_series[1][:training_length])))
        print("------------------------------------------------------------")
        print("Starting evaluation of testing data. Predicting 1 step forward for each delay-vector.")
        print("Testing " + str(len(self._scaled_series[0][(training_length + 1):(training_length + testing_length)])) + " values.")
        print("RMSE Test = " + str(self._pipeline.get_prediction_error(self._scaled_series[0][(training_length + 1):(training_length + testing_length)],
                                                                       self._scaled_series[1][(training_length + 1):(training_length + testing_length)])))
        print("------------------------------------------------------------")
        prediction_length = 10
        print("Starting evaluation of testing data. Predicting " + str(prediction_length) + " steps forward for each delay-vector.")
        print("Not implemented yet.")
        #print("Visualizing results")
        # ToDo: Move visualization to here from pipeline


    def _create_pipeline(self, dimension, level, lambda_parameter, training_accuracy):
        self._scaled_series = PreProcessing().transform_timeseries_to_datatuple(self._timeseries, dimension)
        self._pipeline = TimeSeriesPipeline(training_accuracy)
        self._pipeline.create_learner(level=level, lambda_parameter=lambda_parameter, scaled_samples=self._scaled_series[0][:self._training_length + dimension],
                                      scaled_values=self._scaled_series[1][:self._training_length + dimension], with_adaptivity=self._with_adaptivity)

    def _calculate_henonmap(self, length, a, b, x_0, x_1):
        print("Creating Henon map with parameters: \na = " + str(a) + "\nb = " + str(b))
        values = []
        values.append(x_0)
        values.append(x_1)
        for i in xrange(2, length):
            values.append(a - pow(values[i - 1], 2) + b*values[i - 2])
        print("Calculated Henon map values")
        return values

    def _calculate_jumpmap(self, length, x_0, x_1):
        values = []
        values.append(x_0)
        values.append(x_1)
        for i in xrange(2, length):
            values.append((values[i - 2] + values[i - 1]) % 1)
        print("Calculated Jump map values")
        return values

    def _finance_test(self, s_query):
        data = QuandlDataRetriever().get_financedata(s_query)
        print(data.datasets.keys())
        return data.datasets.get(u'Adj. Close')


