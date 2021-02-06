#!/usr/bin/python
import csv
import numpy as np
import pandas as pd 
import random

DEVTESTSIZE = 2000

trainData = []
devData = []
testData = []

inFile = "finalTrainData.csv"
iTrainFile = open(inFile, "r")
readerTrain = csv.reader(iTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outTrainFile = "modelTrainData.csv"
oTrainFile = open(outTrainFile, "w")
writerTrain = csv.writer(oTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outDevFile = "modelDevData.csv"
oDevFile = open(outDevFile, "w")
writerDev = csv.writer(oDevFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outTestFile = "modelTestData.csv"
oTestFile = open(outTestFile, "w")
writerTest = csv.writer(oTestFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

# randNum = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]
devCount = 0
testCount = 0
for row in readerTrain:
	if row[0] == '':
		continue
	trainDevTest = random.random()
	# if trainDevTest < 0.05 and testCount < DEVTESTSIZE:
###################################################################################################
### only selecting bubble games ###################################################################
###################################################################################################
	gameID = int(row[0])
	if gameID > 21901230:
###################################################################################################
		testCount += 1
		writerTest.writerow(row)

	elif trainDevTest > 0.05 and trainDevTest < 0.1 and devCount < DEVTESTSIZE:
		devCount += 1
		writerDev.writerow(row)
	else:
		writerTrain.writerow(row)
