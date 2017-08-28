import numpy
import os
import pandas
import csv
from model.finance_data import RawFinanceData

class CSVParser(object):             

    def parse_sp500_tickers(self):
        sp500_tickers = []
        with open("../sp500.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for element in row:
                    sp500_tickers.append(element)     
        data = self.parse_tickers()
        sp500_data = []
        counter = 0
        for ticker in sp500_tickers:
            ticker = ticker.strip()
            for item in data:
                name = item.ticker[item.ticker.find("/")+1:].split()[0]
                if name == ticker:   
                    sp500_data.append(item)
        return sp500_data

    def parse_crypto_tickers(self):
        pass

    def parse_tickers(self):
        data = []
        df = pandas.read_csv("../stock_tickers.csv")
        tickers = df["Price"]
        dimensions = df["Embedding_Dimension"]
        names = df["Name"]
        for i in xrange(1, len(tickers)):
            # Check if ticker exists
            if str(tickers[i]) != "nan":
                item = RawFinanceData()
                item.ticker = str(tickers[i])
                # Check if embedding dimension is set
                if str(dimensions[i]) != "nan":
                    item.embedding_dimension = int(dimensions[i])
                item.name = str(names[i])
                data.append(item)
        return data                          

    def write_embedding_dimension(self, ticker, dimension):
        r = csv.reader(open("../stock_tickers.csv"))
        lines = [l for l in r]
        for line in lines:
            if(line[4] == ticker):
                print("Writing embedding dimension")
                line[6] = str(dimension)
        writer = csv.writer(open("../stock_tickers.csv", "w"))
        writer.writerows(lines)

    def write_datasets_to_csv(self, ticker, datasets):
        df = pandas.DataFrame.from_dict(datasets)
        df.to_csv("../quandl_data/{}.csv".format(ticker), sep=",", encoding="utf-8")

    def write_rmses_to_file(self, rmse, path, is_training_set):
        self._check_dir(path)
        df = pandas.DataFrame.from_dict(rmse)
        if is_training_set:
            df.to_csv(path + "/training_errors.csv", sep=",", encoding="utf-8")
        else:
             df.to_csv(path + "/testing_errors.csv", sep=",", encoding="utf-8")

    def read_datasets_from_csv(self, ticker):
        return pandas.DataFrame.from_csv("../quandl_data/{}.csv".format(ticker))

    def write_prediction_results_to_csv(self, results, path):
        self._check_dir(path)
        df = pandas.DataFrame.from_dict(results)
        df.to_csv(path + "/{}.csv".format(ticker))
        
    def _check_dir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)