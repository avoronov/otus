import logging
import sys
from random import shuffle

from .constants import COLUMNS_COUNT, MAX_NUMBER, MIN_NUMBER, ROWS_COUNT

DEFAULT_LOG_LEVEL = logging.ERROR


def get_randomized_number(numbers=None):
    if not numbers:
        numbers = [x for x in range(MIN_NUMBER, MAX_NUMBER + 1)]
        shuffle(numbers)

    for val in numbers:
        yield val


def check_row_and_column(row, column):
    if row > 0 and row <= ROWS_COUNT and column > 0 and column <= COLUMNS_COUNT:
        return True
    return False


loggers = {}


def get_logger(name, level=DEFAULT_LOG_LEVEL):
    global loggers

    if loggers.get(name):
        return loggers.get(name)
    else:
        log = logging.getLogger(name)
        log.setLevel(level)
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )  # %(name)s -
        sh.setFormatter(formatter)
        log.addHandler(sh)
        loggers[name] = log
        return log
