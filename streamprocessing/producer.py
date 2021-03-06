import csv
import datetime
import json
import os
import time

from definitions import ROOT_DIR
from exceptionhandling.catchAndLogExceptions import shutdown_handler
from collect.getTrainInfo import getTrainInfo
from streamprocessing.conf.kafkaconf import Producer, TOPIC_NAME
from logs.loggers import logger, sendMailIfHalts


@sendMailIfHalts(logger)
def producer(filename):
    with open(os.path.join(ROOT_DIR, 'data', filename), 'r') as trenifile:
        numtreni = list(csv.reader(trenifile, delimiter=';'))
        today = datetime.date.today()
        toSkip = {today: []}
        while not shutdown_handler.shutdown:
            today = datetime.date.today()
            if today not in toSkip:
                toSkip = {today: []}
            for row in numtreni:
                numTreno = int(row[0])
                if numTreno not in toSkip[today]:
                    res = getTrainInfo(numTreno)
                    Producer.send(TOPIC_NAME, res)
                    if json.loads(res).get("status", "N/A") == "NotRunningOnDate":
                        toSkip[today].append(numTreno)
                time.sleep(1)
            time.sleep(45)


if __name__ == "__main__":
    producer('numeritreni.csv')
