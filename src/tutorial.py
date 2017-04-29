# Sparse Grids Python Tutorial taken from http://sgpp.sparsegrids.org/example_tutorial_py.html
import pysgpp

def tutorial():
    # define interpolation function
    f = lambda x0, x1: 16.0 * (x0 - 1.0) * x0 * (x1 - 1.0) * x1
    # create 2-dimensional grid with piecewise bilinear basis functions
    dim = 2
    grid = pysgpp.Grid.createLinearGrid(dim)
    # create storage object to access grid nodes etc.
    gridStorage = grid.getStorage()
    print "dimensionality:         {}".format(gridStorage.getDimension())
    # create regular sparse grid of level 3
    level = 3
    grid.getGenerator().regular(level)
    print "number of grid points:  {}".format(gridStorage.getSize())
    # create array wrapper  (coefficient vector for the grid)
    alpha = pysgpp.DataVector(gridStorage.getSize())
    alpha.setAll(0.0)
    print "length of alpha vector: {}".format(len(alpha))
    # loop over all grid points and set initial coefficient
    for i in xrange(gridStorage.getSize()):
      gp = gridStorage.getPoint(i)
      alpha[i] = f(gp.getStandardCoordinate(0), gp.getStandardCoordinate(1))
    print "alpha before hierarchization: {}".format(alpha)
    # hierarchize the coefficient vector
    pysgpp.createOperationHierarchisation(grid).doHierarchisation(alpha)
    print "alpha after hierarchization:  {}".format(alpha)
    # point at which to evaluate grid
    p = pysgpp.DataVector(dim)
    p[0] = 0.52
    p[1] = 0.73
    opEval = pysgpp.createOperationEval(grid)
    print "u(0.52, 0.73) = {}".format(opEval.eval(alpha, p))



