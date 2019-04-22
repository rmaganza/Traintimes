import re
from socket import timeout
from urllib2 import urlopen, URLError

from api.decodingutils import decode_json, decode_lines
from api.retry import retry
from exceptionhandling.catchAndLogExceptions import catchHTTPTimeout
from logs.loggers import logger


def _decode_cercaNumeroTrenoTrenoAutocomplete(s):
    def linefunc(line):
        r = re.search('^(\d+)\s-\s(.+)\|(\d+)-(.+)$', line)
        if r is not None:
            return r.group(2, 4)

    return decode_lines(s, linefunc)


def _decode_autocompletaStazione(s):
    return decode_lines(s, lambda line: tuple(line.strip().split('|')))


class API(object):
    def __init__(self, **options):
        self.__verbose = options.get('verbose', False)
        self.__urlopen = options.get('urlopen', urlopen)
        self.__plainoutput = options.get('plainoutput', False)
        self.__decoders = {
            'andamentoTreno': decode_json,
            'cercaStazione': decode_json,
            'tratteCanvas': decode_json,
            'dettaglioStazione': decode_json,
            'regione': decode_json,
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
