import csv
import os

from getTrainInfo import getTrainInfo

if __name__ == "__main__":
    with open(os.path.join('data', 'numeritreni.csv')) as trenifile:
        numtreni = csv.reader(trenifile, delimiter=';')
        for row in numtreni:
            numTreno = int(row[0])
            if numTreno not in [9517, 9590, 9511, 9548, 9587, 9591, 9608, 9664, 9671, 9717, 9798, 9803, 9810,
                                9421, 9516, 9539, 9540, 9584, 9585, 9611, 9666,
                                8306, 8317]:
                print(getTrainInfo(numTreno))

