import logging.config
import os

from logging_config import LOGGING_CONFIG

def logTrainSearch(log):
    def decorator(func):

        def wrapper(*args, **kwargs):
            if args:
                trainNumber = args[0]
            else:
                trainNumber = kwargs['trainNumber']
            log.info("Searching for train " + str(trainNumber))
            res = func(*args, **kwargs)
            if res.get("status") == "HTTPIssue":
                log.warning(
                    "Train " + str(trainNumber) +
                    " could not be searched. Viaggiatreno is experiencing troubles"
                )
            log.info("Saving info for train " + str(trainNumber))
            return res

        return wrapper

    return decorator


logfolder = os.path.dirname(os.path.abspath(__file__))

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging
