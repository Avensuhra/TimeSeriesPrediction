import numpy
import pandas
import csv
from model.finance_data import RawFinanceData

class CSVParser(object):
    
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

    def read_datasets_from_csv(self, ticker):
        df = pandas.DataFrame.from_csv("../quandl_data/{}.csv".format(ticker))
        