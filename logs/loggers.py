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
            log.info("Sending info for train " + str(trainNumber) + " to consumer")
            return res

        return wrapper

    return decorator


def logWeatherSearch(log):
    def decorator(func):

        def wrapper(*args, **kwargs):
            if args:
                lat, lon = args[0], args[1]
            else:
                lat, lon = kwargs['lat'], kwargs['lon']
            log.info("Fetching weather info for lat " + lat + " and lon: " + lon)
            res = func(*args, **kwargs)
            if res == 1:
                log.info("Could not retrieve weather for lat: " + lat + " and lon: " + lon)
            log.info("Sending weather info to consumer...")
            return res

        return wrapper
    return decorator


logfolder = os.path.dirname(os.path.abspath(__file__))

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging
