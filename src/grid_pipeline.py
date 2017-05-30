import pysgpp
import custom_logger as Log

"""
@Author:    Ingo Mayer
Date:       29.05.2017

Description: Obsolete.

             Sparse grid functionality separated into different callable functions based on the
             pysgpp tutorial. Was intended as basis for future implementations, however this will not
             be possible.
"""

class GridPipeline(object):
    def __init__(self):
        self.grid = None
        self.gridStorage = None
        self.alphas = None
        self.ground_truth = None
        self.function = None
        self.number_of_datapoints = 0
        self.number_of_trainingpoints = 0
        self.dimension = 0

    def create_regular_sparsegrid(self, dimension, level):
        self.dimension = dimension
        Log.info(self.__class__.__name__, "Creating linear grid with dimension " + str(dimension)
                 + " and level " + str(level))
        self.grid = pysgpp.Grid.createLinearGrid(dimension)
        self.gridStorage = self.grid.getStorage()
        self.grid.getGenerator().regular(level)
        Log.info(self.__class__.__name__, "Number of grid points: {}".format(self.gridStorage.getSize()))
        self.alphas = pysgpp.DataVector(self.gridStorage.getSize())
        self.alphas.setAll(0.0)
        Log.info(self.__class__.__name__, "Created alpha vector of size: {}".format(len(self.alphas)))

    # Calculates values at the grid points based on the specified function and sets them as alpha
    def train_grid_with_function(self, function):
        self.use_function = True
        self.function = function
        for i in xrange(self.gridStorage.getSize()):
            gp = self.gridStorage.getPoint(i)
            self.alphas[i] = self.function(gp.getStandardCoordinate(0), gp.getStandardCoordinate(1))
        pysgpp.createOperationHierarchisation(self.grid).doHierarchisation(self.alphas)
        Log.info(self.__class__.__name__, "Alphas after hierarchization: {}".format(self.alphas))

    # Trains the grid with the elements in the dataset
    def train_grid_with_dataset(self, dataset):
        pass

    # Will evaluate the array at all remaining points that were not used for training, only works for dim = 2 atm
    def evaluate_grid_at_vector(self, vector):
        points = pysgpp.DataVector(self.dimension)
        for i in xrange(self.dimension):
            points[i] = vector[i]
        evaluation = pysgpp.createOperationEval(self.grid)
        Log.info(self.__class__.__name__, "Function interpolation value at {0} = {1}".format(vector, evaluation.eval(self.alphas, points)))
        if(self.use_function):
            Log.info(self.__class__.__name__, "Ground truth value at {0} = {1}".format(vector, self.function(vector[0], vector[1])))


    def evaluate_grid_by_dataset(self):
        pass