# system imports
# third party imports
import pysgpp
import tutorial
from grid_pipeline import GridPipeline
from timeseries_pipeline import TimeSeriesPipeline
# application imports
import custom_logger as Log
from test_definitions import HenonTest


def tutorial_test():
    pipeline = GridPipeline()
    pipeline.create_regular_sparsegrid(2, 3)
    function = lambda x0, x1: 16.0 * (x0 - 1.0) * x0 * (x1 - 1.0) * x1
    pipeline.train_grid_with_function(function)
    pipeline.evaluate_grid_at_vector([0.52, 0.73])

def henon_map_test():
    HenonTest(level=3, total_length=20000, training_length=50, a=1.4, b=0.3, x_0=0.1, x_1=0.2)

if __name__ == "__main__":
    Log.init()
    TimeSeriesPipeline().learner_builder_test()
    #tutorial_test()
    #henon_map_test()
