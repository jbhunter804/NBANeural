#!/usr/bin/python
import csv
import random
import numpy as np
import pandas as pd                        

###################################################################################################
###################################################################################################
###################################################################################################
### MUST USE fixWL_trainData.py FIRST ###
###################################################################################################
###################################################################################################
###################################################################################################


##inFile has meta data on where last cut off due to server issues. Will resume collecting there###
inFile = "fixedWL_trainData.csv"
iTrainFile = open(inFile, "r")
readerTrain = csv.reader(iTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outTrainFile = "fixedDataDupExamples.csv"
oTrainFile = open(outTrainFile, "w")
writerTrain = csv.writer(oTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
for row in readerTrain:
#################################
# readerTrain[0] = headers
# readerTrain[row][0] = gameid
# readerTrain[row][1] = team1 Win 
# readerTrain[row][2] = team1 score
# readerTrain[row][3] = team2 score
# readerTrain[row][4] = is team1 home?
# readerTrain[row][4:707] = team1 data
# readerTrain[row][5] = is team2 home?
# readerTrain[row][708:] = team2 data
	currentRow = []
	if row[0] == '':
		writerTrain.writerow(row)
		continue
	currentRow.append(row[0])
#### write the original row ######	
	writerTrain.writerow(row)

###################################################################################################
################################# isolating bubble games from duplication #########################
###################################################################################################
	gameID = int(row[0])
	if gameID > 21901230:
		continue
###################################################################################################
#### switch w/l before team data is swapped
	if int(row[1]) > 0:
		currentRow.append(0)
	else:
		currentRow.append(1)
#### switch team1 and 2 point totals
	currentRow.append(row[3])
	currentRow.append(row[2])

#### write team2 Data 
	for i in range(707,len(row)):
		currentRow.append(row[i])

#### write team1 Data 
	for i in range(4,707):
		currentRow.append(row[i])
	writerTrain.writerow(currentRow)
	# print(currentRow)


iTrainFile.close()
oTrainFile.close()
