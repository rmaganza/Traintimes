import csv
import datetime
import os
import time

from definitions import ROOT_DIR
from exceptionhandling.catchAndLogExceptions import sendMailIfHalts, shutdown_handler
from getTrainInfo import getTrainInfo
from kafkaconf import Producer, TOPIC_NAME
from logs.loggers import logger


@sendMailIfHalts(logger)
def producer(filename):
    with open(os.path.join(ROOT_DIR, 'data', filename)) as trenifile:
        numtreni = csv.reader(trenifile, delimiter=';')
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
                if res.get("status", "N/A") == "NotRunningOnDate":
                    toSkip[today].append(numTreno)
        time.sleep(1)


if __name__ == "__main__":
    producer('numeritreni.csv')
