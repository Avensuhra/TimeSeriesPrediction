import sys
import numpy as np
import qdarkstyle
import pandas
import matplotlib.pyplot as plot
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication, QInputDialog, QColorDialog

class Visualization(object):
    _app = None
    _win = None
    _plot = None

    def __init__(self):
        pass
        """
        self._app = QtGui.QApplication([])
        self._win = pg.GraphicsWindow(title="Basic plotting examples")
        self._win.resize(1000,600)
        self._win.setWindowTitle('pyqtgraph example: Plotting')
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        self._plot = self._win.addPlot(title="Timeseries Prediction"
        """

    def plot_groundtruth(self, values):
        self._plot.plot(values, pen=(255, 0, 0), name="Real Values")

    def plot_prediction(self, values):
        self._plot.plot(values, pen=(0, 255, 0), name="Predicted Values")

    def plot_statistic(self):
        pass

    def plot_rmse_evolution(self): 
        app = QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        fig, ax = plot.subplots()
        
        add_line = True
        while(add_line): 
            add_file = True  
            averages = []
            while(add_file):
                # select rmse files
                dialog = QFileDialog()
                dialog.exec_()
                file = dialog.selectedFiles()[0]
                averages.append(pandas.DataFrame.from_csv(file)['rmse'].mean())
                reply = QMessageBox.question(None, 'User Input', "Do you want to add aother file?", QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.No:
                    add_file = False
            text, ok = QInputDialog.getText(None, 'User Dialog', 'Enter line name:')
            #col = QColorDialog.getColor()
            ax.plot(averages, 'r--')
            reply = QMessageBox.question(None, 'User Input', "Do you want to add another line?", QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                add_line = False

            plot.show()
            

            
        # add line
        # calculate average for each file
        # plot line
        # add another line?
