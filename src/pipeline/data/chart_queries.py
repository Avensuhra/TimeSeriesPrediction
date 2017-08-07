# system imports
import json
import requests
import time
import numpy
import pandas
from datetime import datetime
# third party imports
import quandl
# application imports
from model.finance_data import RawFinanceData

class QuandlDataRetriever(object):
    api_key = "FKDJP8dGxEuWKyjEGzby"

    def __init__(self):
        quandl.ApiConfig.api_key = self.api_key

    def get_financedata(self, s_query):
        data = self._data_query(s_query)
        return self._parse_to_financedata(data)

    def _metadata_query(self, s_query):
        payload = {'api_key': self.api_key}
        query = requests.get("https://www.quandl.com/api/v3/datasets/{}/metadata.json".format(s_query), params=payload)
        if (query.status_code == requests.codes.ok):
            return json.loads(query.text)
        else:
            print("Quandl API request failed with error " + str(query.status_code))

    def _data_query(self, s_query):
        try:
            query = quandl.get(s_query, authtoken="FKDJP8dGxEuWKyjEGzby")
            return query
        except Exception as e:
            print(str(e))

    def _parse_to_financedata(self, data):
        parsed_data = RawFinanceData()
        parsed_data.datasets = data
        dates = parsed_data.datasets.index.values
        timestamps = []
        for i in xrange(0, len(dates)):
            timestamp = (dates[i] - numpy.datetime64('1970-01-01T00:00:00Z')) / numpy.timedelta64(1, 's')
            timestamps.append(timestamp)
        parsed_data.datasets["timestamps"] = pandas.Series(timestamps, index=parsed_data.datasets.index)
        return parsed_data