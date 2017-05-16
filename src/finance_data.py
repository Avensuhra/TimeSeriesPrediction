# system imports
# third party imports
# application imports
import custom_logger as Log

class FinanceData(object):
    def __init__(self):
        self.open = []
        self.close = []
        self.high = []
        self.low = []
        self.adjusted_close = []

