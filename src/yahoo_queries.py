# system imports
import requests
from dateutil import parser
# third party imports
# application imports
import custom_logger as Log

class YahooQueries(object):

    def historical_query(self, end, start, symbol):
        Log.debug(self.__class__.__name__, "Attempting Yahoo historical query with daterange {0} - {1} and symbol {2}".format(start, end, symbol))
        try:
            end_date = parser.parse(end, dayfirst=True)
            start_date = parser.parse(start, dayfirst=True)
        except Exception as e:
            Log.error(self.__class__.__name__, str(e))
            return None

        payload = {"s" : symbol, "d" : end_date.month - 1, "e" : end_date.day, "f" : end_date.year,
                   "a" : start_date.month - 1, "b" : start_date.day, "c" : start_date.year, "ignore" : ".csv"}
        Log.debug(self.__class__.__name__, "Yahoo histrocial query payload assembled.")
        url = "http://real-chart.finance.yahoo.com/table.csv"
        query = requests.get(url, params=payload)
        if (query.status_code == requests.codes.ok):
            Log.debug(self.__class__.__name__, "Yahoo historical query succeeded.")
            return query.text
        else:
            Log.error(self.__class__.__name__, "Yahoo historical query failed with code {}".format(query.status_code))
            return None

    def query_to_finance_data(self):
        pass