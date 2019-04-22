from backports.functools_lru_cache import lru_cache

from api.meteo.callweatherAPI import callweatherAPI
from logs.loggers import logger


@lru_cache(maxsize=10000)
def getweather(lat, lon, numtrain, date):
    meteo = {}
    if numtrain and date:
        res = callweatherAPI(lat, lon)
    else:
        return meteo

    if res == 1:
        logger.info("Could not retrieve weather for lat: " + lat + " and lon: " + lon)
        return meteo
    else:
        meteoinfo = res["observations"]["location"]["observation"]
        meteo["skydescription"] = meteoinfo["skyDescription"]
        meteo["temp"] = meteoinfo["temperature"]
        meteo["precipitations"] = meteoinfo["precipitation3H"]
        meteo["wind"] = meteoinfo["windSpeed"]
        meteo["visibility"] = meteoinfo["visibility"]
        meteo["snow"] = meteoinfo["snowcover"]
        return meteo
