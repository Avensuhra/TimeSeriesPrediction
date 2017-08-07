# system imports
import os
# third party imports
import scipy
# application imports
#from pipeline.data.reference_tests import TimeseriesTest, TestTypes
from pipeline.pipeline import Pipeline


#def henon_map_test():
#    TimeseriesTest(type=TestTypes.HENON , dimension= 2, level=3, training_length=50,
#                   lambda_parameter=pow(2, -17), training_accuracy=pow(10, -13))

#def jumpmap_test():
#    TimeseriesTest(type=TestTypes.JUMP_MAP, dimension=5, level=5, training_length=50,
#                   lambda_parameter=pow(10, -4), training_accuracy=pow(10, -13))

def finance_test():
    Pipeline(500, True, pow(10, -4), 3).run()
    #TimeseriesTest(type=TestTypes.FINANCIAL_DATA, dimension=2, level=8, training_length=5000, testing_length=10,
     #              lambda_parameter=pow(10, -4), training_accuracy=pow(10, -13), quandl_query="WIKI/AAPL", with_adaptivity=False)

if __name__ == "__main__":
    #henon_map_test()
    #jumpmap_test()
    finance_test()
