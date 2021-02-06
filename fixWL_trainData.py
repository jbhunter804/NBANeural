#!/usr/bin/python
import csv
import random
import numpy as np
import pandas as pd                        

##inFile has meta data on where last cut off due to server issues. Will resume collecting there###
inFile = "testtrainData.csv"
iTrainFile = open(inFile, "r")
readerTrain = csv.reader(iTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outTrainFile = "fixedWL_trainData.csv"
oTrainFile = open(outTrainFile, "w")
writerTrain = csv.writer(oTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
for row in readerTrain:
#################################
# readerTrain[0] = headers
# readerTrain[row][0] = gameid
# readerTrain[row][1] = homeWin 
# readerTrain[row][2] = team1 score
# readerTrain[row][3] = team2 score
# readerTrain[row][4] = is team1 home?
# readerTrain[row][5:707] = team1 data
# readerTrain[row][708:] = team2 data
	currentRow = []
	if row[0] == '':
		writerTrain.writerow(row)
		continue
	currentRow.append(row[0])
	if (row[2]) > (row[3]):
		currentRow.append(1)
	else:
		currentRow.append(0)
	for i in range(2,len(row)):
		currentRow.append(row[i])
	writerTrain.writerow(currentRow)
	# print(currentRow)


iTrainFile.close()
oTrainFile.close()


