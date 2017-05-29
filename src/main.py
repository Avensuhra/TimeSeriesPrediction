# system imports
# third party imports
import pysgpp
import tutorial
from grid_pipeline import GridPipeline
# application imports
import custom_logger as Log


if __name__ == "__main__":
    Log.init()
    pipeline = GridPipeline()
    pipeline.create_regular_sparsegrid(2, 3)
    function = lambda x0, x1: 16.0 * (x0 - 1.0) * x0 * (x1 - 1.0) *x1
    pipeline.train_grid_with_function(function)
    pipeline.evaluate_grid_at_vector([0.52, 0.73])