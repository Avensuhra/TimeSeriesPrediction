# system imports
import os
# third party imports
# application imports
from test_definitions import TimeseriesTest, TestTypes


def henon_map_test():
    TimeseriesTest(type=TestTypes.HENON ,dimension= 2, level=6, total_length=20000, training_length=500, lambda_parameter=pow(2, -25), training_accuracy=0.00000000103)

if __name__ == "__main__":
    henon_map_test()
