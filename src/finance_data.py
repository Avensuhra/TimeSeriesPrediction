# system imports
import json
import requests
import time
# third party imports
import quandl
# application imports


class FinanceData(object):
    def __init__(self):
        self.datasets = {}
        self.timestamps = []
        self.name = ""
        self.description = ""

class QuandlDataRetriever(object):
    api_key = "FKDJP8dGxEuWKyjEGzby"

    def __init__(self):
        quandl.ApiConfig.api_key = self.api_key

    def get_financedata(self, s_query):
        metadata = self._metadata_query(s_query).get("dataset")
        data = self._data_query(s_query)
        return self._parse_to_financedata(metadata, data)

    def _metadata_query(self, s_query):
        payload = {'api_key': self.api_key}
        query = requests.get("https://www.quandl.com/api/v3/datasets/{}/metadata.json".format(s_query), params=payload)
        if (query.status_code == requests.codes.ok):
            return json.loads(query.text)
        else:
            print("Quandl API request failed with error " + str(query.status_code))

    def _data_query(self, s_query):
        try:
            query = quandl.get(s_query, authtoken="FKDJP8dGxEuWKyjEGzby", returns="numpy")
            return query
        except Exception as e:
            print(str(e))

    def _parse_to_financedata(self, metadata, data):
        parsed_data = FinanceData()
        parsed_data.name = metadata.get("name")
        parsed_data.description = metadata.get("description")
        meta_columns = metadata.get("column_names")

        prices = []
        for i in range(1, len(meta_columns)):
            prices.append([])
        for tuple in data:

            parsed_data.timestamps.append(int((time.mktime(tuple[0].timetuple()) + tuple[0].microsecond/1000000.0)))
            for i in range(1, len(tuple)):
                prices[i - 1].append(tuple[i])
        for i in range(1, len(meta_columns)):
            parsed_data.datasets[meta_columns[i]] = prices[i - 1]
        return parsed_data