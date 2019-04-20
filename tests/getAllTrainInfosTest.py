import csv
import os

from definitions import ROOT_DIR
from getTrainInfo import getTrainInfo

with open(os.path.join(ROOT_DIR, 'data', 'numeritreni.csv')) as trenifile:
    numtreni = csv.reader(trenifile, delimiter=';')

for row in numtreni:
    numTreno = int(row[0])
    res = getTrainInfo(numTreno)
    print(res)