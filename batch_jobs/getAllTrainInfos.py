import csv
import os

from definitions import ROOT_DIR
from getTrainInfo import getTrainInfo
from exceptionhandling.catchAndLogExceptions import sendMailIfHalts
from logs.logger import logger


@sendMailIfHalts(logger)
def getAllTrainInfos(filename):
    with open(os.path.join(ROOT_DIR, 'data', filename)) as trenifile:
        numtreni = csv.reader(trenifile, delimiter=';')
        for row in numtreni:
            numTreno = int(row[0])
            if numTreno not in [9517, 9590, 9511, 9548, 9587, 9591, 9608, 9664, 9671, 9717, 9798, 9803, 9810,
                                9421, 9516, 9539, 9540, 9584, 9585, 9611, 9666,
                                8306, 8317]:
                print(getTrainInfo(numTreno))


if __name__ == "__main__":
    getAllTrainInfos('numeritreni.csv')