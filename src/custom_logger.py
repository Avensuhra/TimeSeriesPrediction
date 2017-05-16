# system imports
import logging
from datetime import datetime
# third party imports
# application imports

def init():
    logging.basicConfig(filename="../log/tsp.log", format="%(levelname)s(%(message)s", level=logging.DEBUG)


def info(source, text):
    logging.info("{0} {1}: {2}".format(get_time_string(), source, text))


def debug(source, text):
    logging.debug("{0} {1}: {2}".format(get_time_string(), source, text))


def warning(source, text):
    logging.warning("{0} {1}: {2}".format(get_time_string(), source, text))


def error(source, text):
    logging.error("{0} {1}: {2}".format(get_time_string(), source, text))


def get_time_string():
    time = datetime.now()
    time_string = "{0}:{1}:{2}".format(time.hour, time.day, time.second)
    return time_string

