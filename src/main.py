# system imports
import os
# third party imports
# application imports
import logging as Log
from test_definitions import HenonTest
from timeseries_learner import CustomLearner
from pre_processing import PreProcessing

def henon_map_test():
    HenonTest(level=7, total_length=20000, training_length=5000, a=1.4, b=0.3, x_0=0.1, x_1=0.2, lambda_parameter=pow(2, -22))


def calculate_timeseries(length, a, b, x_0, x_1):
    values = []
    values.append(x_0)
    values.append(x_1)
    for i in xrange(2, length):
        values.append(a - pow(values[i - 1], 2) + b*values[i - 2])
    return values

def test_custom_learner():
    learner = CustomLearner(2, 3, pow(2, -17))
    timeseries = calculate_timeseries(20000, 1.4, 0.3, 0.1, 0.2)
    scaled_series = PreProcessing().transform_timeseries_to_datatuple(timeseries[:(50 + 2)], 2)
    learner.set_training_data(scaled_series[0], scaled_series[1])

if __name__ == "__main__":
    try:
        os.remove("./log/tsp.log")
    except:
        None
    format = "[%(filename)s:%(lineno)s - %(funcName)s() ]\t\t%(message)s"
    Log.basicConfig(filename="./log/tsp.log", format=format, level=Log.DEBUG)
    #henon_map_test()
    test_custom_learner()
