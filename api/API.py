import datetime
import json
import re
from socket import timeout
from urllib2 import urlopen, URLError

from collect.weather.conf import METEO_CONF
from exceptionhandling.catchAndLogExceptions import catchHTTPTimeout
from exceptionhandling.retry import retry
from logs.loggers import logger, logWeatherSearch


class API(object):
    def __init__(self, **options):
        self.__verbose = options.get('verbose', False)
        self.__urlopen = options.get('urlopen', urlopen)
        self.__plainoutput = options.get('plainoutput', False)
        self.__decoders = {
            'andamentoTreno': self._decode_json,
            'cercaStazione': self._decode_json,
            'tratteCanvas': self._decode_json,
            'dettaglioStazione': self._decode_json,
            'regione': self._decode_json,
            'cercaNumeroTrenoTrenoAutocomplete': self._decode_cercaNumeroTrenoTrenoAutocomplete,
            'autocompletaStazione': self._decode_autocompletaStazione
        }
        self.__default_decoder = lambda x: x

    @staticmethod
    def _check_timestamp(ts):
        return (ts is not None) and (ts > 0) and (ts < 2147483648000)

    @staticmethod
    def convert_timestamp(ts):
        return datetime.datetime.fromtimestamp(ts / 1000)

    @staticmethod
    def check_timestamp(ts):
        return (ts is not None) and (ts > 0) and (ts < 2147483648000)

    def _decode_json(self, s):
        if s == '':
            return None
        return json.loads(s)

    def _decode_lines(self, s, linefunc):
        if s == '':
            return []

        lines = s.strip().split('\n')
        result = []
        for line in lines:
            result.append(linefunc(line))

        return result

    def _decode_cercaNumeroTrenoTrenoAutocomplete(self, s):
        def linefunc(line):
            r = re.search('^(\d+)\s-\s(.+)\|(\d+)-(.+)$', line)
            if r is not None:
                return r.group(2, 4)

        return self._decode_lines(s, linefunc)

    def _decode_autocompletaStazione(self, s):
        return self._decode_lines(s, lambda line: tuple(line.strip().split('|')))

    def format_timestamp(self, ts, fmt="%H:%M:%S"):
        if self.check_timestamp(ts):
            return self.convert_timestamp(ts).strftime(fmt)
        else:
            return 'N/A'

    def __checkAndDecode(self, function, data):
        decoder = self.__decoders.get(function, self.__default_decoder)
        return decoder(data)

    @catchHTTPTimeout
    @retry((URLError, timeout), logger=logger)
    def callviaggiatreno(self, function, *params, **options):
        plain = options.get('plainoutput', self.__plainoutput)
        verbose = options.get('verbose', self.__verbose)

        base = 'http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/'
        path = '/'.join(str(p) for p in params)
        url = base + function + '/' + path

        if verbose:
            logger.info("Calling URL " + url)

        req = self.__urlopen(url)

        data = req.read().decode('utf-8')
        if plain:
            return data
        else:
            return self.__checkAndDecode(function, data)

    @logWeatherSearch(logger)
    @catchHTTPTimeout
    @retry((URLError, timeout), logger=logger)
    def callweatherAPI(self, lat, lon):
        url = "https://weather.cit.api.here.com/weather/1.0/report.json" \
              "?product=observation&latitude=%(lat)s&longitude=%(lon)s&oneobservation=true" \
              "&app_id=%(appid)s&app_code=%(appcode)s" % {
                  "lat": lat, "lon": lon, "appid": METEO_CONF["APP_ID"],
                  "appcode": METEO_CONF["APP_CODE"]
              }

        req = urlopen(url.encode("utf8"))

        data = req.read().decode("utf8")

        return self._decode_json(data)
