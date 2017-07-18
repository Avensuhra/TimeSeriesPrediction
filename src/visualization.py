from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg


class Visualization(object):
    _app = None
    _win = None
    _plot = None

    def __init__(self):
        self._app = QtGui.QApplication([])
        self._win = pg.GraphicsWindow(title="Basic plotting examples")
        self._win.resize(1000,600)
        self._win.setWindowTitle('pyqtgraph example: Plotting')
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        self._plot = self._win.addPlot(title="Timeseries Prediction")

    def plot_groundtruth(self, values):
        self._plot.plot(values, pen=(255, 0, 0), name="Real Values")

    def plot_prediction(self, values):
        self._plot.plot(values, pen=(0, 255, 0), name="Predicted Values")

    def plot_statistic(self):
        pass

