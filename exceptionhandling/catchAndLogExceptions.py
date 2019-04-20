from socket import timeout
from urllib2 import URLError
from functools import wraps


def log_and_send_mail(logger, e):
    logger.critical("*CRITICAL ERROR* Program stopped working for exception " + repr(e), exc_info=True)


def sendMailIfHalts(logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except StandardError as e:
                # log the exception
                log_and_send_mail(logger, e)
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

