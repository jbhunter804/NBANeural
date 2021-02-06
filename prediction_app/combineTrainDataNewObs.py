#!/usr/bin/python
import csv

trainFile = "modelDevData.csv"
oTrainFile = open(trainFile, "a")
writerTrain = csv.writer(oTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

gameFile = "nextDataForModel.csv"
oGameFile = open(gameFile, "r")
readerGame = csv.reader(oGameFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

for game in readerGame:
	writerTrain.writerow(game)