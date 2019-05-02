# coding=UTF-8

from socket import timeout
from urllib2 import URLError, urlopen

from api.decodingutils import decode_json
from api.meteo.conf import METEO_CONF
from exceptionhandling.retry import retry
from exceptionhandling.catchAndLogExceptions import catchHTTPTimeout
from logs.loggers import logger, logWeatherSearch


@logWeatherSearch(logger)
@catchHTTPTimeout
@retry((URLError, timeout), logger=logger)
def callweatherAPI(lat, lon):
    url = "https://weather.cit.api.here.com/weather/1.0/report.json" \
          "?product=observation&latitude=%(lat)s&longitude=%(lon)s&oneobservation=true" \
          "&app_id=%(appid)s&app_code=%(appcode)s" % {
              "lat": lat, "lon": lon, "appid": METEO_CONF["APP_ID"],
              "appcode": METEO_CONF["APP_CODE"]
          }

    req = urlopen(url.encode("utf8"))

    data = req.read().decode("utf8")

    return decode_json(data)
