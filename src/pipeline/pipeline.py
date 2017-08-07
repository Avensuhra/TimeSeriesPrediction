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


from preprocessing.csv_parser import CSVParser
from .data.chart_queries import QuandlDataRetriever
import nolds
import math
import os.path


class Pipeline(object):
    _data = None
    _training_length = None
    _adaptivity = None
    _regression_parameter = None
    _grid_level = None

    def __init__(self, training_length, use_adaptivity, regression_parameter, grid_level):
        self._training_length = training_length
        self._adaptivity = use_adaptivity
        self._regression_parameter = regression_parameter
        self._grid_level = grid_level

    def run(self):
        print("General Parameters: ")
        print("Lambda: {}".format(self._regression_parameter))
        print("Grid level: {}".format(self._grid_level))
        print("Adaptivity: {}".format(self._adaptivity))
        print("Training length: {}".format(self._training_length))
        self._get_tickers()
        print("Evaluating {} companies.".format(len(self._data)))
        print("------------------------------------------------------------")
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
            # Check for embedding dimension
            if element.embedding_dimension == 0:
                element.embedding_dimension = self._calculate_embedding_dimension(dataset)
                CSVParser().write_embedding_dimension(element.ticker, element.embedding_dimension)
            print("Embedding dimension is {}".format(element.embedding_dimension))
            # Build learner
            # Train learner
            # start prediction loop
            # write results to file
            # evaluate results

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

    def _build_learner(self):
        pass

    def _start_prediction(self):
        pass

    def _evaluate_results(self):
        pass

