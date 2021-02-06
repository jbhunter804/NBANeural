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
inFile = "fixedDataDupExamples.csv"
iTrainFile = open(inFile, "r")
readerTrain = csv.reader(iTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outTrainFile = "allExamples.csv"
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
# readerTrain[row][5:707] = team1 player data
# readerTrain[row][4] = is team2 home?
# readerTrain[row][709:] = team2 player data
	if row[0] == '':
		writerTrain.writerow(row)
		continue
###################################################################################################
################################# isolating bubble games from duplication #################################
###################################################################################################
	gameID = int(row[0])
	if gameID > 21901230:
		writerTrain.writerow(row)
		continue
###################################################################################################

	playerData = {0: row[5:122], 1:row[122:239], 2:row[239:356], 3:row[356:473], 4:row[473:590], 5:row[590:707], 6: row[708:825],7: row[825:942],8:row[942:1059], 9:row[1059:1176], 10:row[1176:1293], 11:row[1293:1410]}
	for i in range(6):
		currentRow = []
		currentTeam1 = row[:5]
		currentTeam2 = []
		# for c in range(107):
		# 	currentTeam1.append(playerData[i][c]) #append player a data
		# 	currentTeam2.append()
		for j in range(6):
			# if j != i: #when not player a, append players b-f
			for c in range(117):
				currentTeam1.append(playerData[((i+j)%6)][c])
				currentTeam2.append(playerData[((i+j)%6)+6][c])
		currentTeam1.append(row[707]) #append team2 HV
		for a in range(len(currentTeam1)):
			currentRow.append(currentTeam1[a])
		for a in range(len(currentTeam2)):
			currentRow.append(currentTeam2[a])

		# for i2 in range(7,10):
		# 	currentRow = []
		# 	currentTeam2 = []
		# 	for c in range(107):
		# 		currentTeam2.append(playerData[i2][c]) 
		# 	for j2 in range(7,13):
		# 		if j != i: #when not player a, append players b-f
		# 			for c in range(107):
		# 				currentTeam1.append(playerData[((i+j)%6)+1][c])
		# 	for a in range(len(currentTeam1)):
		# 		currentRow.append(currentTeam1[a])
		# 	for a in range(len(currentTeam2)):
		# 		currentRow.append(currentTeam2[a])
		writerTrain.writerow(currentRow)


iTrainFile.close()
oTrainFile.close()
