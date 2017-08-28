"""
Author: Ingo Mayer
Purpose: Full pipeline for a sparse grid prediction for financial timeseries

Conventions (a.k.a. read this if you're running into errors):
1.  The RawFinancialData Class has to be used for all steps prior to the actual training & testing of the sparse grids
    This includes the parsed data received from Quandl, the parsing of data from CSV files & the embedding dimension calculation
2.  The member "datasets" in the RawFinancialData class needs to be a pandas Dataframe that contains a column called "timestamps" with 
    exactly that as content. Having the dates as index (which is default for Quandl queries) is not enough!
3.  Only use the run() function outside of this class. The pipeline requires a strict workflow
4.  Try to use already downloaded data, retrieving data & calculating embedding dimensions for 3000+ companies takes a while
"""

from pysgpp.extensions.datadriven.learner import SolverTypes
from preprocessing.csv_parser import CSVParser
from timeseries_learner import TimeseriesLearner
from preprocessing.pre_processing import PreProcessing
from .data.chart_queries import QuandlDataRetriever
from postprocessing import error_calculation as error_functions
from datetime import datetime, date, timedelta
import nolds
import math
import os.path


class FinancePipeline(object):
    _data = None
    _startdate_train = None
    _enddate_train = None
    _startdate_test = None
    _enddate_test = None
    _adaptivity = None
    _adapt_threshold = None
    _adapt_rate = None
    _regression_parameter = None
    _grid_level = None
    _dimension = None
    _training_accuracy = None
    _training_length = None
    _learner = None
    _test_type = None
    _number_companies = None
    _retrain = None
    _prediction_steps = None

    def __init__(self):
        pass

    @property
    def grid_level(self):
        return self._grid_level

    @grid_level.setter
    def grid_level(self, value):
        self._grid_level = value

    @property
    def adaptivity(self):
        return self._adaptivity

    @adaptivity.setter
    def adaptivity(self, value):
        self._adaptivity = value

    @property 
    def adapt_threshold(self):
        return self._adapt_threshold

    @adapt_threshold.setter
    def adapt_threshold(self, value):
        self._adapt_threshold = value

    @property
    def adapt_rate(self):
        return self._adapt_rate

    @adapt_rate.setter
    def adapt_rate(self, value):
        self._adapt_rate = value

    @property
    def regression_parameter(self):
        return self._regression_parameter

    @regression_parameter.setter
    def regression_parameter(self, value):
        self._regression_parameter = value

    @property
    def accuracy(self):
        return self._training_accuracy

    @accuracy.setter
    def accuracy(self, value):
        self._training_accuracy = value

    @property
    def startdate_train(self):
        return self._startdate_train

    @startdate_train.setter
    def startdate_train(self, value):
        self._startdate_train = value

    @property
    def enddate_train(self):
        return self._enddate_train

    @enddate_train.setter
    def enddate_train(self, value):
        self._enddate_train = value
        value = value + timedelta(days=1)
        self._startdate_test = value

    @property
    def enddate_test(self):
        return self._enddate_test

    @enddate_test.setter
    def enddate_test(self, value):
        self._enddate_test = value

    @property 
    def training_length(self):
        return self._training_length

    @training_length.setter
    def training_length(self, value):
        self._training_length = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self._number_companies = len(self._data)

    @property
    def test_type(self):
        return self._test_type

    @test_type.setter
    def test_type(self, value):
        self._test_type = value

    @property
    def retrain(self):
        return self._retrain

    @retrain.setter
    def retrain(self, value):
        self._retrain = value

    @property 
    def prediction_steps(self):
        return self._prediction_steps

    @prediction_steps.setter
    def prediction_steps(self, value):
        self._prediction_steps = value

    def run(self):
        print("General Parameters: ")
        print("Lambda: {}".format(self._regression_parameter))
        print("Grid level: {}".format(self._grid_level))
        print("Adaptivity: {}".format(self._adaptivity))
        print("Training length: {}".format(self._training_length))
        print("Evaluating {} companies.".format(len(self._data)))
        print("------------------------------------------------------------")
        folder_name = "../results/FinanceData/l{0}_c{1}_{2}".format(self._grid_level, 
                                                                         self._number_companies, self._test_type)
        if self._retrain:
            folder_name += "_r{}".format(self._prediction_steps)
        training_errors = {}
        training_errors["ticker"] = []
        training_errors["rmse"] = []
        testing_errors = {}
        testing_errors["ticker"] = []
        testing_errors["rmse"] = []
        # Loop over each dataset
        for element in self._data:
            print("Starting Evaluation for {}".format(element.name))
            # Get data from Quandl or csv file if already downloaded
            tmp_name = element.ticker[element.ticker.find("/")+1:].split()[0]
            if os.path.isfile("../quandl_data/{}.csv".format(tmp_name)):
                element.datasets = CSVParser().read_datasets_from_csv(tmp_name)
            else:   
                parsed_data = QuandlDataRetriever().get_financedata(element.ticker)
                element.datasets = parsed_data.datasets
                # write data to file so it doesn't have to be downloaded again
                CSVParser().write_datasets_to_csv(tmp_name, element.datasets)
            # Always use adjusted close for now
            dataset = element.datasets.get(u'Adj. Close')
            # Split dataset into training and test set according to selected dates
            training_set = dataset[str(self._startdate_train):str(self._enddate_train)]
            testing_set = dataset[str(self._startdate_test):str(self._enddate_test)]
            print len(training_set), len(testing_set)
            if len(training_set) == 0 or len(testing_set) == 0:
                print("Not enough data to test this company.")
                continue;
            # Check for embedding dimension
            if element.embedding_dimension == 0:
                element.embedding_dimension = self._calculate_embedding_dimension(dataset)
                CSVParser().write_embedding_dimension(element.ticker, element.embedding_dimension)
            print("Embedding dimension is {}".format(element.embedding_dimension))
            # Taken's delay embedding theorem
            self._dimension = 2*element.embedding_dimension + 1
            print("Converting data into dimensional construct.")
            scaled_training_delayvectors = self._prepare_single_dataset(training_set)
            scaled_testing_delayvectors = self._prepare_single_dataset(testing_set)
            # Build learner
            training_samples = scaled_training_delayvectors[0]
            training_values = scaled_training_delayvectors[1]
            print("Training with {} values.".format(len(training_samples)))
            self._build_learner(training_samples, training_values)
            training_errors["rmse"].append((self._get_prediction_error(training_samples, training_values)))
            training_errors["ticker"].append(element.ticker)
            print("Training finished.")   
            testing_samples = scaled_testing_delayvectors[0]
            testing_values = scaled_testing_delayvectors[1]
            print("Testing with {} values.".format(len(testing_samples)))
            print("Retraining after every {} prediction steps".format(self._prediction_steps))
            while len(testing_samples) > self._prediction_steps:
                testing_subset_samples = testing_samples[:self._prediction_steps]
                testing_subset_values = testing_values[:self._prediction_steps]
                testing_errors["rmse"].append((self._get_prediction_error(testing_subset_samples, testing_subset_values)))
                testing_errors["ticker"].append(element.ticker)
                # retrain with testing samples & values
                self.retrain_learner(testing_subset_samples, testing_subset_values)
                # remove used values
                testing_samples = testing_samples[self._prediction_steps:]
                testing_values =  testing_values[self._prediction_steps:]
            print("Testing finished.") 
            print("------------------------------------------------------------")  
        CSVParser().write_rmses_to_file(training_errors, folder_name, True)
        CSVParser().write_rmses_to_file(testing_errors, folder_name, False)   

    def _get_prediction_error(self, samples, values):
        prediction_vector = []
        for i in xrange(len(samples)):
            prediction_vector.append(self._learner.predict_next_value(samples[i]))
        return error_functions.rmse(prediction_vector, values)

    # Grassberger-Procaccia algorithm
    def _calculate_embedding_dimension(self, dataset):
        embedding_dims = []
        for i in xrange(1, 101):
            embedding_dims.append(nolds.corr_dim(dataset[:self._training_length], i))
        max_dim = max(embedding_dims)
        # round for 2 digits accuracy
        if(100*max_dim%100 < 50):
            return int(math.floor(max_dim))
        else:
            return int(math.ceil(max_dim))

    def _prepare_single_dataset(self, dataset):
        return PreProcessing().transform_timeseries_to_datatuple(dataset, self._dimension)

    def _build_learner(self, training_samples, training_values):
        self._learner = TimeseriesLearner()
        self._learner.set_training_data(training_samples, training_values)
        self._learner.set_grid(self._grid_level)
        self._learner.set_specification(self._regression_parameter, self._adaptivity)
        self._learner.set_stop_policy()
        self._learner.set_solver(SolverTypes.CG, self._training_accuracy)
        self._learner.get_result()

    def retrain_learner(self, training_samples, training_values):
        self._learner.set_training_data(training_samples, training_values)
        self._learner.retrain()
        
