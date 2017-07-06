# system imports
import os
# third party imports
# application imports
import logging as Log
from timeseries_pipeline import TimeSeriesPipeline
from test_definitions import HenonTest


# outdated
def henon_map_test():
    HenonTest(level=6, total_length=20000, training_length=500, a=1.4, b=0.3, x_0=0.1, x_1=0.2, lambda_parameter=pow(2, -25))

if __name__ == "__main__":
    try:
        os.remove("./log/tsp.log")
    except:
        None
    format = "[%(filename)s:%(lineno)s - %(funcName)s() ]\t\t%(message)s"
    Log.basicConfig(filename="./log/tsp.log", format=format, level=Log.DEBUG)
    #train_file = "../TimeSeriesPrediction/datasets/bank_rejections/bank8FM_train.arff"
    #TimeSeriesPipeline().create_learner_with_file(3, pow(2, -17), train_file)
    henon_map_test()
