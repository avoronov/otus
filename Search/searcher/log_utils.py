import logging
import sys

DEFAULT_LOG_LEVEL = logging.ERROR

def set_debug_log_level():
    DEFAULT_LOG_LEVEL = logging.DEBUG

def set_error_log_level():
    DEFAULT_LOG_LEVEL = logging.ERROR

def get_logger(level=DEFAULT_LOG_LEVEL):
    log = logging.getLogger(__name__)
    log.setLevel(level)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') # %(name)s - 
    sh.setFormatter(formatter)
    log.addHandler(sh)
    return log