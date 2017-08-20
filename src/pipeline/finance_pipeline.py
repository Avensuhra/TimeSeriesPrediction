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
import nolds
import math
import os.path


class FinancePipeline(object):
    _data = None
    _training_length = None
    _adaptivity = None
    _regression_parameter = None
    _grid_level = None
    _dimension = None
    _training_accuracy = None
    _learner = None
    _test_type = None
    _number_companies = None

    def __init__(self, training_length, use_adaptivity, regression_parameter, grid_level, training_accuracy, test_type, number_of_companies):
        self._training_length = training_length
        self._adaptivity = use_adaptivity
        self._regression_parameter = regression_parameter
        self._grid_level = grid_level
        self._training_accuracy = training_accuracy
        self._test_type = test_type
        self._number_companies = number_of_companies

    def run(self):
        print("General Parameters: ")
        print("Lambda: {}".format(self._regression_parameter))
        print("Grid level: {}".format(self._grid_level))
        print("Adaptivity: {}".format(self._adaptivity))
        print("Training length: {}".format(self._training_length))
        self._get_tickers()
        print("Evaluating {} companies.".format(len(self._data)))
        print("------------------------------------------------------------")
        folder_name = "../results/FinanceData/l{0}_t{1}_c{2}_{3}".format(self._grid_level, self._training_length,   
                                                                         self._number_companies, self._test_type)
        training_errors = {}
        training_errors["ticker"] = []
        training_errors["rmse"] = []
        testing_errors = {}
        testing_errors["ticker"] = []
        testing_errors["rmse"] = []
        # Loop over each dataset
        for element in self._data[:self._number_companies]:
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
            # Check for embedding dimension
            if element.embedding_dimension == 0:
                element.embedding_dimension = self._calculate_embedding_dimension(dataset)
                CSVParser().write_embedding_dimension(element.ticker, element.embedding_dimension)
            print("Embedding dimension is {}".format(element.embedding_dimension))
            # Taken's delay embedding theorem
            self._dimension = 2*element.embedding_dimension + 1
            print("Converting data into dimensional construct.")
            scaled_delay_vectors = self._prepare_single_dataset(dataset)
            print("Number of total delay vectors: {}".format(len(scaled_delay_vectors[0])))
            if(len(scaled_delay_vectors[0]) <= self._training_length):
                print("Insufficient data. Skipping this company.")
                continue;
            # Build learner
            training_samples = scaled_delay_vectors[0][:self._training_length]
            training_values = scaled_delay_vectors[1][:self._training_length]
            print("Training with {} values.".format(len(training_samples)))
            self._build_learner(training_samples, training_values)
            training_errors["rmse"].append((self._get_prediction_error(training_samples, training_values)))
            training_errors["ticker"].append(element.ticker)
            print("Training finished.")   
            testing_samples = scaled_delay_vectors[0][self._training_length:]
            testing_values = scaled_delay_vectors[1][self._training_length:]
            print("Testing with {} values.".format(len(testing_samples)))
            testing_errors["rmse"].append((self._get_prediction_error(testing_samples, testing_values)))
            testing_errors["ticker"].append(element.ticker) 
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

    def _get_tickers(self):
        self._data = CSVParser().parse_tickers()

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

    def _start_prediction(self):
        pass
