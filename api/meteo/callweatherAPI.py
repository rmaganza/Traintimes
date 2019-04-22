from socket import timeout
from urllib2 import URLError, urlopen

from api.decodingutils import decode_json
from api.meteo.conf import METEO_CONF
from api.retry import retry
from exceptionhandling.catchAndLogExceptions import catchHTTPTimeout
from logs.loggers import logger


@catchHTTPTimeout
@retry((URLError, timeout), logger=logger)
def callweatherAPI(lat, lon):
    url = "https://weather.cit.api.here.com/weather/1.0/report.json" \
          "?product=observation&latitude=%(lat)f&longitude=%(lon)f&oneobservation=true" \
          "&app_id=%(appid)s&app_code=%(appcode)s" % {
              "lat": lat, "lon": lon, "appid": METEO_CONF["APP_ID"],
              "appcode": METEO_CONF["APP_CODE"]
          }

    req = urlopen(url)

    data = req.read().decode("utf8")

    return decode_json(data)