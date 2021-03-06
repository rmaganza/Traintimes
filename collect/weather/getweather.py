from backports.functools_lru_cache import lru_cache

from api.API import API
from logs.loggers import logger


@lru_cache(maxsize=10000)
def getweather(lat, lon, numtrain, date):
    meteo = {}
    if numtrain and date:
        api = API()
        res = api.callweatherAPI(lat, lon)
    else:
        logger.warning("Missing arguments to properly make weather call")
        return meteo

    if res == 1 or res is None:
        return meteo
    else:
        meteoinfo = res["observations"]["location"][0]['observation'][0]
        meteo["skydescription"] = meteoinfo.get("skyDescription")
        meteo["temp"] = meteoinfo.get("temperature")
        meteo["precipitations"] = meteoinfo.get("precipitation3H")
        meteo["wind"] = meteoinfo.get("windSpeed")
        meteo["visibility"] = meteoinfo.get("visibility")
        meteo["snow"] = meteoinfo.get("snowCover")
        return meteo
