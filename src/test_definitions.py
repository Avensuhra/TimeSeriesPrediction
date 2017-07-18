# standard imports
from enum import Enum

# third party imports
# application imports
from timeseries_pipeline import TimeSeriesPipeline
from pre_processing import PreProcessing
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

    def __init__(self, type, dimension, level, total_length, training_length, lambda_parameter, training_accuracy, quandl_query = ""):
        print("General Parameters: ")
        print("Lambda: " + str(lambda_parameter))
        print("Grid level: " + str(level))
        print("Total datapoints: " + str(total_length))
        print("Training datapoints: " + str(training_length))
        self._training_length = training_length
        print("------------------------------------------------------------")
        if(type == TestTypes.HENON):
            self._timeseries = self._calculate_henonmap(total_length, a=1.4, b=0.3, x_0=0.1, x_1=0.2)
        elif(type == TestTypes.JUMP_MAP):
            self._timeseries = self._calculate_jumpmap(total_length, 0.1, 0.2)
        elif(type == TestTypes.ANN_COMPETITION):
            raise NotImplementedError("Ann Competition not implented yet.")
        elif (type == TestTypes.FINANCIAL_DATA):
            self._timeseries = self._finance_test(quandl_query)
            print(len(self._timeseries))
            total_length = len(self._timeseries)
            # ToDo: Parse finance_data to dimensional data construct
            # ToDo: Decide which chart source to use (e.g. closed, open, etc..) or all of them?

        print("------------------------------------------------------------")
        print("Starting training")
        self._create_pipeline(dimension, level, lambda_parameter, training_accuracy)
        print("Finished training")
        print("------------------------------------------------------------")
        print("Starting evaluation of training data")
        print("Testing " + str(training_length) + " values.")
        print("RMSE Train = " + str(self._pipeline.get_prediction_error(self._scaled_series[0][:training_length + dimension], self._scaled_series[1][:training_length + dimension])))
        print("------------------------------------------------------------")
        print("Starting evaluation of testing data")
        print("Testing " + str(total_length - training_length) + " values.")
        print("RMSE Test = " + str(self._pipeline.get_prediction_error(self._scaled_series[0][(training_length - dimension):], self._scaled_series[1][(training_length - dimension):])))
        print("------------------------------------------------------------")
        print("Visualizing results")
        # ToDo: Move visualization to here from pipeline


    def _create_pipeline(self, dimension, level, lambda_parameter, training_accuracy):
        self._scaled_series = PreProcessing().transform_timeseries_to_datatuple(self._timeseries, dimension)
        self._pipeline = TimeSeriesPipeline(training_accuracy)
        self._pipeline.create_learner(level=level, lambda_parameter=lambda_parameter, scaled_samples=self._scaled_series[0][:self._training_length + dimension],
                                      scaled_values=self._scaled_series[1][:self._training_length + dimension])

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


