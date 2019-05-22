import signal
from functools import wraps
from socket import timeout
from urllib2 import URLError

from logs.loggers import logger


class ShutdownHandler(object):
    shutdown = False

    def __init__(self, log):
        signal.signal(signal.SIGTERM, self.shutdown_detected)
        self.logger = log

    def shutdown_detected(self, signum, frame):
        self.shutdown = True
        self.logger.critical("*CRITICAL* DETECTED SHUTDOWN. Aborting...")


def catchHTTPTimeout(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (URLError, timeout):
            return 1
    return wrapper


shutdown_handler = ShutdownHandler(logger)
