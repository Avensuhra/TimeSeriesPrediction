# system imports
import os
import sys
# third party imports
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QCheckBox
from PyQt5.QtWidgets import QCalendarWidget, QComboBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

class GUI(QWidget):
    _manager = None

    def __init__(self, manager):
        super(GUI, self).__init__()
        self._manager = manager
        self.init_ui()        
        self.set_standard_values()
        self.init_communication()    

    def init_ui(self):
        self.setWindowTitle('Financial Time Series Prediction')         
        self.show()
        layout = QGridLayout()
        self.grid_setup = GridSetupGUI()
        self.data_setup = DataSetupGUI()
        layout.addWidget(self.grid_setup, 0, 0, QtCore.Qt.AlignTop)
        layout.addWidget(self.data_setup, 0, 1, QtCore.Qt.AlignTop)
        self.run_button = QPushButton("Run Pipeline")
        layout.addWidget(self.run_button, 1, 0, 1, 2)
        self.setLayout(layout)

    def set_standard_values(self):
        self.grid_setup.level.setText("3")
        self.grid_setup.regression_parameter_base.setText("10")
        self.grid_setup.regression_parameter_exponent.setText("-4")
        self.grid_setup.accuracy_base.setText("10")
        self.grid_setup.accuracy_exponent.setText("-15")
        self.grid_setup.use_adaptivity.setChecked(True)
        self.grid_setup.adapt_rate.setText("0.1")
        self.grid_setup.adapt_threshold.setText("0.01")
        startdate_train = QtCore.QDate()
        startdate_train.setDate(2000, 1, 1)
        enddate_train = QtCore.QDate()
        enddate_train.setDate(2010, 12, 31)
        enddate_test = QtCore.QDate()
        enddate_test.setDate(2016, 12, 31)
        self.data_setup.startdate_train.setSelectedDate(startdate_train)
        self.data_setup.enddate_train.setSelectedDate(enddate_train)
        self.data_setup.enddate_test.setSelectedDate(enddate_test)
        self.grid_setup.retrain.setChecked(True)
        self.grid_setup.prediction_steps.setText("5")

    def init_communication(self):
        self.run_button.clicked.connect(self._manager.run_pipeline)


class GridSetupGUI(QWidget):
    def __init__(self):
        super(GridSetupGUI, self).__init__()
        self.init_ui()        

    def init_ui(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Grid Setup:"), 0, 0)
        self.level = QLineEdit()
        layout.addWidget(QLabel("Level: "), 1, 0)
        layout.addWidget(self.level, 1, 1)
        self.regression_parameter_base = QLineEdit()
        self.regression_parameter_exponent = QLineEdit()
        layout.addWidget(QLabel("Reg. Parameter:"), 2, 0)
        layout.addWidget(self.regression_parameter_base, 2, 1)
        layout.addWidget(QLabel("pow"), 2, 2)
        layout.addWidget(self.regression_parameter_exponent, 2, 3)
        self.accuracy_base = QLineEdit()
        self.accuracy_exponent = QLineEdit()
        layout.addWidget(QLabel("Accuracy:"), 3, 0)
        layout.addWidget(self.accuracy_base, 3, 1)
        layout.addWidget(QLabel("pow"), 3, 2)
        layout.addWidget(self.accuracy_exponent, 3, 3)
        self.use_adaptivity = QCheckBox()
        layout.addWidget(QLabel("Adaptivity:"), 4, 0)
        layout.addWidget(self.use_adaptivity, 4, 1)
        self.adapt_threshold = QLineEdit()
        layout.addWidget(QLabel("Adapt. Threshold:"), 5, 0)
        layout.addWidget(self.adapt_threshold, 5, 1)
        self.adapt_rate = QLineEdit()
        layout.addWidget(QLabel("Adapt. Rate:"), 6, 0)
        layout.addWidget(self.adapt_rate, 6, 1)
        self.retrain = QCheckBox()
        layout.addWidget(QLabel("Retrain"), 7, 0)
        layout.addWidget(self.retrain, 7, 1)
        self.prediction_steps = QLineEdit()
        layout.addWidget(QLabel("Retrain after steps:"), 8, 0)
        layout.addWidget(self.prediction_steps, 8, 1)
        self.setLayout(layout)


class DataSetupGUI(QWidget):
    def __init__(self):
        super(DataSetupGUI, self).__init__()
        self.init_ui()        
    
    def init_ui(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Data Setup:"), 0, 0)
        self.source = QComboBox()
        self.source.addItem("SP500")
        self.source.addItem("Crypto")
        layout.addWidget(QLabel("Source:"), 1, 0)
        layout.addWidget(self.source, 1, 1)
        self.startdate_train = QCalendarWidget()
        layout.addWidget(QLabel("Start Date (train):"), 2, 0)
        layout.addWidget(self.startdate_train, 2, 1)
        self.enddate_train = QCalendarWidget()
        layout.addWidget(QLabel("End Date (train):"), 3, 0)
        layout.addWidget(self.enddate_train, 3, 1)
        self.enddate_test = QCalendarWidget()
        layout.addWidget(QLabel("End Date (test):"), 4, 0)
        layout.addWidget(self.enddate_test, 4, 1)
        self.setLayout(layout)
