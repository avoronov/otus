import logging
import sys

DEFAULT_LOG_LEVEL = logging.DEBUG # logging.CRITICAL 

def get_logger(level=DEFAULT_LOG_LEVEL):
    log = logging.getLogger(__name__)
    log.setLevel(level)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') # %(name)s - 
    sh.setFormatter(formatter)
    log.addHandler(sh)
    return log