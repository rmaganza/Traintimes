# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import json
import os
import sys
from collections import OrderedDict

from api.API import API
from collect.weather.getweather import getweather
from definitions import ROOT_DIR
from logs.loggers import logger, logTrainSearch


def getStationsLatLon(stationName, stationInfoDict):
    filterStations = [stat for stat in stationInfoDict if stat["name"] == stationName]

    lat = filterStations[0].get("lat")
    lon = filterStations[0].get("lon")

    return lat, lon


@logTrainSearch(logger)
def callApiAndGetResults(trainNumber, departures, res, api):
    # each result has two elements, the name of the station [0] and its ID [1].
    # we only care about the first result here
    # Therefore, departures[0][1] is the station ID element #1 of the first result [0].

    departure_ID = departures[0][1]

    # This fetches the status for that train number from that departure_ID we just fetched.
    # It is required by viaggiatreno.it APIs.
    train_status = api.callviaggiatreno('andamentoTreno', departure_ID, trainNumber)

    if not train_status or train_status == 1:
        logger.warning("Could not collect data for train " + str(trainNumber))
        return {}

    else:
        res["departureDay"] = datetime.date.today().strftime("%Y-%m-%d")
        # in these cases, the train has been cancelled.
        if train_status['tipoTreno'] == 'ST' or train_status['provvedimento'] == 1:
            res["status"] = "cancelled"

        # otherwise, it is checked whether the train is running or if it's not yet.
        elif train_status['oraUltimoRilevamento'] is None:
            res["status"] = "notDeparted"
            res["isRunning"] = "no"
            res["lastCheckedAt"] = "N/A"
            res["scheduledDeparture"] = api.format_timestamp(train_status['orarioPartenza'])
            res["origin"] = train_status["origine"]

        # finally, if the train is up and running
        else:
            if train_status['tipoTreno'] in ('PP', 'SI', 'SF'):
                res["status"] = "partiallyCancelled"

            else:
                res["status"] = "OK"

            res["lastCheckedAt"] = train_status["stazioneUltimoRilevamento"]
            res["lastCheckedTime"] = api.format_timestamp(train_status["oraUltimoRilevamento"])

            with open(os.path.join(ROOT_DIR, 'data', 'stations-dump', 'stations.json')) as jsonfile:
                station_infos = json.load(jsonfile)

            station_infos = tuple(station_infos)
            stops = []
            delays = []
            if train_status['fermate']:
                for f in train_status['fermate']:
                    station = f["stazione"]
                    stop = OrderedDict([('station', station),
                                        ('scheduledAt', api.format_timestamp(f['programmata']))])

                    lat, lon = getStationsLatLon(station, station_infos)
                    stop["lat"], stop["lon"] = lat, lon

                    if f['tipoFermata'] == 'P':
                        stop["actual"] = api.format_timestamp(f['partenzaReale'])
                        stop["delay"] = f['ritardoPartenza']
                        stop["descr"] = 'Departure'
                    else:
                        stop["actual"] = api.format_timestamp(f['arrivoReale'])
                        stop["delay"] = f['ritardoArrivo']
                        stop["descr"] = 'Arrival'
                        stop["weather"] = getweather(lat, lon, trainNumber, res["departureDay"])

                    delays.append(stop["delay"])

                    if len(delays) > 1:
                        stop["delayDiff"] = delays[-1] - delays[-2]

                    if f['actualFermataType'] == 3:
                        stop["status"] = "Cancelled"

                    elif f['actualFermataType'] == 0:
                        stop["status"] = "N/A"

                    else:
                        stop["status"] = "OK"

                    # there we go
                    stops.append(stop)

                actualStops = [stop for stop in stops if stop["status"] != "N/A"]
                res["stops"] = actualStops

                if len(actualStops) == len(stops):
                    res["isRunning"] = "Arrived"

                    if stops[0]["scheduledAt"] != "N/A" and stops[-1]["scheduledAt"] != "N/A":
                        scheduledDeparture = datetime.datetime.strptime(stops[0]["scheduledAt"], "%H:%M:%S")
                        scheduledArrival = datetime.datetime.strptime(stops[-1]["scheduledAt"], "%H:%M:%S")
                        timediff = scheduledArrival - scheduledDeparture
                        res["scheduledTripDuration"] = timediff.seconds / 60
                        res["finalDelay"] = stops[-1]["delay"]

                else:
                    res["isRunning"] = "running"

            else:
                logger.warning("Problem in collecting stops data for train " + str(trainNumber))

            if res.get("finalDelay"):
                res["status"] = "Arrived"

    return res


def getTrainInfo(trainNumber):
    res = OrderedDict([('trainNumber', trainNumber)])

    api = API()

    # "cercaNumeroTrenoTrenoAutocomplete is the viaggiatreno API call that returns the starting station
    # for the train number specified as its argument.
    # Unfortunately that could return more than one station.
    departures = api.callviaggiatreno('cercaNumeroTrenoTrenoAutocomplete', trainNumber)

    if departures != 1:
        if len(departures) == 0:
            logger.info("Train {0} not found on date.".format(trainNumber))
            res["status"] = "NotRunningOnDate"
            return json.dumps(res)

        elif len(departures) > 1:
            departures = departures[0]

        res = callApiAndGetResults(trainNumber, departures, res, api)

    return json.dumps(res).encode('utf-8')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: " + os.path.basename(__file__) + " <trainNumber>")
        sys.exit()

    trainNumber = int(sys.argv[1])

    print(getTrainInfo(trainNumber))
