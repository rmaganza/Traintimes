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


shutdown_handler = ShutdownHandler(logger)


def log_critical_and_send_mail(log, e):
    log.critical("*CRITICAL ERROR* Program stopped working for exception " + repr(e), exc_info=True)


def sendMailIfHalts(log):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param log: The logging object
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except StandardError as e:
                # log the exception
                log_critical_and_send_mail(log, e)
                # re-raise the exception
                raise

        return wrapper

    return decorator


def catchHTTPTimeout(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (URLError, timeout):
            return 1
    return wrapper

