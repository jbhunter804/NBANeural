#!/usr/bin/python
import csv
import random
import numpy as np
import pandas as pd                        


def moneyLine_to_pct(mlOdd):
	answer = 0
	if mlOdd < 0:
		answer = (-1* mlOdd)/((-1*mlOdd)+100)
	else:
		answer = 100/(100+mlOdd)
	return answer

inFile19 = "csvOdds/gameIDodds2019.csv"
iTrainFile19 = open(inFile19, "r")
readerTrain19 = csv.reader(iTrainFile19, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

inFile18 = "csvOdds/gameIDodds2018.csv"
iTrainFile18 = open(inFile18, "r")
readerTrain18 = csv.reader(iTrainFile18, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

inFile17 = "csvOdds/gameIDodds2017.csv"
iTrainFile17 = open(inFile17, "r")
readerTrain17 = csv.reader(iTrainFile17, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

inFile16 = "csvOdds/gameIDodds2016.csv"
iTrainFile16 = open(inFile16, "r")
readerTrain16 = csv.reader(iTrainFile16, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

inFileTrain = "allExamples.csv"
# inFileTrain = "fixedDataDupExamples.csv"
iTrainFile = open(inFileTrain, "r")
readerTrain = csv.reader(iTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outTrainFile = "finalTrainData.csv"
oTrainFile = open(outTrainFile, "w")
writerTrain = csv.writer(oTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

allOdds= {}
####create dict of all games in form (gameID)+H/V/N#####
lastGameID = ''
count = 0
for row in readerTrain19:
	if lastGameID == row[0]:
		count = 1
	else:
		count = 0
	if row[1] == 'N' and count == 0:
		allOdds[row[0]+row[1]+'1'] = [row[-1],row[3]]
		# print("added a team1")
	elif row[1] == 'N' and count == 1:
		allOdds[row[0]+row[1]+'2'] = [row[-1],row[3]]
		# print("added a team2")
	else:
		allOdds[row[0]+row[1]] = [row[-1],row[3]]
	lastGameID = row[0]
for row in readerTrain18:
	allOdds[row[0]+row[1]] = [row[-1],row[3]]
for row in readerTrain17:
	allOdds[row[0]+row[1]] = [row[-1],row[3]]
for row in readerTrain16:
	allOdds[row[0]+row[1]] = [row[-1],row[3]]
# print(allOdds)
########################################
########################################
for row in readerTrain:
	currentRow = []
	team1Odds = 0
	team2Odds = 0
	if row[0] == '':
		continue

	try:
		mlHOdds = int(allOdds['00' + row[0]+'H'][0])
		mlVOdds = int(allOdds['00' + row[0]+'V'][0])
		pctHOdds = moneyLine_to_pct(mlHOdds)
		pctVOdds = moneyLine_to_pct(mlVOdds)

		if int(row[4]) == 1: ###if team1 is home
			# print("team1 is home")
			team1Odds = pctHOdds
			team2Odds = pctVOdds
		else: #### if team1 is visitor
			# print("team1 is visitor")
			team1Odds = pctVOdds
			team2Odds = pctHOdds
		### copy all data from training example
		for i in range(len(row)):
			currentRow.append(row[i])
		### add implied team1 and 2 odds 
		currentRow.append(team1Odds)
		currentRow.append(team2Odds)
		writerTrain.writerow(currentRow)
	except:
		try:
			# print("no clear Home/Visitor - " + row[0])
			team1Score = int(row[2])
			team2Score = int(row[3])
			# print('00' + row[0]+'N1')
			teamHScore = int(allOdds['00' + row[0]+'N1'][1])
			# print(teamHScore)
			teamVScore = int(allOdds['00' + row[0]+'N2'][1])
			# print("found team scores in odds dict")
			mlHOdds = int(allOdds['00' + row[0]+'N1'][0])
			mlVOdds = int(allOdds['00' + row[0]+'N2'][0])
			pctHOdds = moneyLine_to_pct(mlHOdds)
			pctVOdds = moneyLine_to_pct(mlVOdds)
			### if team1/home is team 1
			if teamHScore == team1Score:
				team1Odds = pctHOdds
				team2Odds = pctVOdds
			#if team1/home is team2
			elif teamHScore == team2Score:
				team1Odds = pctVOdds
				team2Odds = pctHOdds
			else:
				print("didn't match a team to a team in game " + row[0])
			for i in range(len(row)):
				currentRow.append(row[i])
			### add implied team1 and 2 odds 
			currentRow.append(team1Odds)
			currentRow.append(team2Odds)
			writerTrain.writerow(currentRow)


		except:
			print("this game is just weird - " + row[0])
			continue





