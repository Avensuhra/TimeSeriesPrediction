# system imports
from pipeline_manager import PipelineManager
from pipeline.preprocessing.csv_parser import CSVParser
from pipeline.data.reference_tests import TimeseriesTest, TestTypes

def henon_map_test():
    TimeseriesTest(type=TestTypes.HENON , dimension= 2, level=7, training_length=5000,
    lambda_parameter=pow(2, -22), training_accuracy=pow(10, -20))

def jumpmap_test():
    TimeseriesTest(type=TestTypes.JUMP_MAP, dimension=5, level=5, training_length=5000,
                   lambda_parameter=pow(10, -4), training_accuracy=pow(10, -13))


if __name__ == "__main__":
    henon_map_test()
    #jumpmap_test()
    #PipelineManager()    