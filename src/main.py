# system imports
import os
# third party imports
# application imports
from test_definitions import TimeseriesTest, TestTypes


def henon_map_test():
    TimeseriesTest(type=TestTypes.HENON , dimension= 2, level=3, total_length=20000, training_length=50,
                   lambda_parameter=pow(2, -17), training_accuracy=pow(10, -10))

def jumpmap_test():
    TimeseriesTest(type=TestTypes.JUMP_MAP, dimension=5, level=5, total_length=20000, training_length=5000,
                   lambda_parameter=pow(10, -4), training_accuracy=pow(10, -10))

def finance_test():
    TimeseriesTest(type=TestTypes.FINANCIAL_DATA, dimension=5, level=5, total_length=20000, training_length=5000,
                   lambda_parameter=pow(10, -4), training_accuracy=pow(10, -10), quandl_query="WIKI/AAPL")

if __name__ == "__main__":
    #henon_map_test()
    #jumpmap_test()
    finance_test()