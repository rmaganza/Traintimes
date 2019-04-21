import json
import re
from api import dateutils
from socket import timeout
from logs.loggers import logger
from exceptionhandling.catchAndLogExceptions import catchHTTPTimeout
from retry import retry

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen, URLError

logger = logger.getLogger("API")


def train_runs_on_date(train_info, date):
    # trainInfo['runs_on'] flag:
    # G    Runs every day
    # FER5 Runs only Monday to Friday (holidays excluded)
    # FER6 Runs only Monday to Saturday (holidays excluded)
    # FEST Runs only on Sunday and holidays
    runs_on = train_info.get('runs_on', 'G')
    suspended = train_info.get('suspended', [])

    for from_, to in suspended:
        ymd = date.strftime('%Y-%m-%d')
        if from_ <= ymd <= to:
            return False

    if runs_on == 'G':
        return True

    wd = date.weekday()

    if runs_on == 'FEST':
        return dateutils.is_holiday(date) or wd == 6

    if dateutils.is_holiday(date):
        return False

    if runs_on == 'FER6' and wd < 6:
        return True
    if runs_on == 'FER5' and wd < 5:
        return True

    return False


# Decoders for API Output - TODO: Proper error handling
def _decode_json(s):
    if s == '':
        return None
    return json.loads(s)


def _decode_lines(s, linefunc):
    if s == '':
        return []

    lines = s.strip().split('\n')
    result = []
    for line in lines:
        result.append(linefunc(line))

    return result


def _decode_cercaNumeroTrenoTrenoAutocomplete(s):
    def linefunc(line):
        r = re.search('^(\d+)\s-\s(.+)\|(\d+)-(.+)$', line)
        if r is not None:
            return r.group(2, 4)

    return _decode_lines(s, linefunc)


def _decode_autocompletaStazione(s):
    return _decode_lines(s, lambda line: tuple(line.strip().split('|')))


class API(object):
    def __init__(self, **options):
        self.__verbose = options.get('verbose', False)
        self.__urlopen = options.get('urlopen', urlopen)
        self.__plainoutput = options.get('plainoutput', False)
        self.__decoders = {
            'andamentoTreno': _decode_json,
            'cercaStazione': _decode_json,
            'tratteCanvas': _decode_json,
            'dettaglioStazione': _decode_json,
            'regione': _decode_json,
            'cercaNumeroTrenoTrenoAutocomplete': _decode_cercaNumeroTrenoTrenoAutocomplete,
            'autocompletaStazione': _decode_autocompletaStazione
        }
        self.__default_decoder = lambda x: x

    def __checkAndDecode(self, function, data):
        decoder = self.__decoders.get(function, self.__default_decoder)
        return decoder(data)

    @catchHTTPTimeout
    @retry((URLError, timeout), logger=logger)
    def call(self, function, *params, **options):
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
