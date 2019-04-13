# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os
import json
import datetime
from backports.functools_lru_cache import lru_cache
import viaggiatreno


def is_valid_timestamp(ts):
    return (ts is not None) and (ts > 0) and (ts < 2147483648000)


def format_timestamp(ts, fmt='%H:%M:%S'):
    if is_valid_timestamp(ts):
        return datetime.datetime.fromtimestamp(ts / 1000).strftime(fmt)
    else:
        return 'N/A'


@lru_cache(maxsize=1500)
def getStationsLatLon(stationName, stationInfoDict):
    filterStations = [stat for stat in stationInfoDict if stat["name"] == stationName]

    lat = filterStations[0].get("lat")
    lon = filterStations[0].get("lon")

    return lat, lon


if __name__ == '__main__':
    if len(sys.argv) < 2:
        import os

        print("Usage: " + os.path.basename(__file__) + " <trainNumber>")
        sys.exit()

    trainNumber = int(sys.argv[1])

    with open(os.path.join('data', 'stations-dump', 'stations.json')) as jsonfile:
        station_infos = json.dump(jsonfile)

    api = viaggiatreno.API()

    # "cercaNumeroTrenoTrenoAutocomplete is the viaggiatreno API call that returns the starting station
    # for the train number specified as its argument.
    # Unfortunately that could return more than one station.
    departures = api.call('cercaNumeroTrenoTrenoAutocomplete', trainNumber)

    if len(departures) == 0:
        print("Train {0} does not exists.".format(trainNumber))
        sys.exit()

    # TODO: handle not unique train numbers, when len(departures) > 1

    # each result has two elements, the name of the station [0] and its ID [1].
    # we only care about the first result here
    # Therefore, departures[0][1] is the station ID element #1 of the first result [0].
    departure_ID = departures[0][1]

    # This fetches the status for that train number from that departure_ID we just fetched.
    # It is required by viaggiatreno.it APIs.
    train_status = api.call('andamentoTreno', departure_ID, trainNumber)

    res = {"trainNumber": trainNumber}
    # in these cases, the train has been cancelled.
    if train_status['tipoTreno'] == 'ST' or train_status['provvedimento'] == 1:
        res["status"] = "cancelled"

    # otherwise, it is checked whether the train is running or if it's not yet.
    elif train_status['oraUltimoRilevamento'] is None:
        res["status"] = "notDeparted"
        res["scheduledDeparture"] = format_timestamp(train_status['orarioPartenza'])
        res["origin"] = train_status["origine"]

    # finally, if the train is up and running
    else:
        if train_status['tipoTreno'] in ('PP', 'SI', 'SF'):
            res["status"] = "partiallyCancelled"

        else:
            res["status"] = "OK"

        res["lastCheckedStation"] = train_status["stazioneUltimoRilevamento"]
        res["lastCheckedTime"] = format_timestamp(train_status["oraUltimoRilevamento"])

        stops = []
        for f in train_status['fermate']:
            station = f["stazione"]
            stop = {'station': station,
                    "scheduledAt": format_timestamp(f['programmata'])}

            stop["lat"], stop["lon"] = getStationsLatLon(station, station_infos)

            if f['tipoFermata'] == 'P':
                stop["actual"] = format_timestamp(f['partenzaReale'])
                stop["delay"] = f['ritardoPartenza']
                stop["descr"] = 'Departure'
            else:
                stop["actual"] = format_timestamp(f['arrivoReale'])
                stop["delay"] = f['ritardoArrivo']
                stop["descr"] = 'Arrival'

            # the output line is formatted according to the available data:
            if f['actualFermataType'] == 3:
                stop["status"] = "Cancelled"
            elif f['actualFermataType'] == 0:
                stop["status"] = "N/A"
            else:
                stop["status"] = "OK"

            # there we go
            stops.append(stop)

        res["stops"] = stops
    print(json.dumps(res))
