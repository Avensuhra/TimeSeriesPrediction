import sys
from enum import Enum
import qdarkstyle
from view.gui import GUI
from pipeline.finance_pipeline import FinancePipeline
from pipeline.preprocessing.csv_parser import CSVParser
from PyQt5.QtWidgets import QApplication


class DataSource(Enum):
    sp500 = 0,
    crypto = 1


class PipelineManager(object):
    _gui = None
    _pipeline = None
 
    def __init__(self):
        self._pipeline = FinancePipeline()
        app = QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self._gui = GUI(self)
        sys.exit(app.exec_())

    def run_pipeline(self):
        self._pipeline.grid_level = int(self._gui.grid_setup.level.text())
        self._pipeline.regression_parameter = pow(int(self._gui.grid_setup.regression_parameter_base.text()), 
        int(self._gui.grid_setup.regression_parameter_exponent.text()))
        self._pipeline.accuracy = pow(int(self._gui.grid_setup.accuracy_base.text()), 
        int(self._gui.grid_setup.accuracy_exponent.text()))
        self._pipeline.adaptivity = self._gui.grid_setup.use_adaptivity.isChecked()
        if(self._pipeline.adaptivity):
            self._pipeline.adapt_threshold = float(self._gui.grid_setup.adapt_threshold.text())
            self._pipeline.adapt_rate = float(self._gui.grid_setup.adapt_rate.text())
        self._pipeline.training_length = 500
        self._prepare_data()

    def _prepare_data(self):
        if(self._gui.data_setup.source.currentIndex() == DataSource.sp500.value[0]):
            print("Selected sp500 as data source.")
            data = CSVParser().parse_sp500_tickers()
            self._pipeline.data = data
            if self._pipeline.adaptivity:
                self._pipeline.test_type = "sp500_adaptiveGrid"
            else:
                self._pipeline.test_type = "sp500_regGrid"
        else:
            print("crypto - todo") 
        startdate = self._gui.data_setup.startdate_train.selectedDate().toPyDate()
        self._pipeline.startdate_train = startdate
        enddate_train = self._gui.data_setup.enddate_train.selectedDate().toPyDate()
        self._pipeline.enddate_train = enddate_train
        enddate_test = self._gui.data_setup.enddate_test.selectedDate().toPyDate()    
        self._pipeline.enddate_test = enddate_test
        self._pipeline.retrain = self._gui.grid_setup.retrain.isChecked()
        self._pipeline.prediction_steps = int(self._gui.grid_setup.prediction_steps.text())
        self._pipeline.run()        

    def finance_test(self):
        for level in xrange(3, 10):
            FinancePipeline(training_length=500, use_adaptivity=False, regression_parameter=pow(10, -4), grid_level=level,
                            training_accuracy=pow(10, -13), test_type="regGrid", number_of_companies=500).run()
        #TimeseriesTest(type=TestTypes.FINANCIAL_DATA, dimension=2, level=8, training_length=5000, testing_length=10,
        #              lambda_parameter=pow(10, -4), training_accuracy=pow(10, -13), quandl_query="WIKI/AAPL", with_adaptivity=False)
