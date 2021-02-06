#!/usr/bin/python
import csv
import random
import numpy as np
import pandas as pd                        

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

inFile15 = "csvOdds/gameIDodds2015.csv"
iTrainFile15 = open(inFile15, "r")
readerTrain15 = csv.reader(iTrainFile15, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

inFileTrain = "testtrainData.csv"
# inFileTrain = "fixedDataDupExamples.csv"
iTrainFile = open(inFileTrain, "r")
readerTrain = csv.reader(iTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outTrainFile = "fixedWL_trainData.csv"
oTrainFile = open(outTrainFile, "w")
writerTrain = csv.writer(oTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

allScores= {}

for row in readerTrain19:
	allScores[row[0]+row[1]] = int(row[-4])
for row in readerTrain18:
	allScores[row[0]+row[1]] = int(row[-4])
for row in readerTrain17:
	allScores[row[0]+row[1]] = int(row[-4])
for row in readerTrain16:
	allScores[row[0]+row[1]] = int(row[-4])
for row in readerTrain15:
	allScores[row[0]+row[1]] = int(row[-4])

for row in readerTrain:
	currentRow = [row[0]]
	team1Score = 0
	team2Score = 0
	team1Home = 0
	team2Home = 0
	try:
		if row[0] == '':
			continue
		HScore = int(allScores["00"+row[0]+'H'])
		VScore = int(allScores["00"+row[0]+'V'])
		# print(str(row[0]))
		if int(row[2]) == HScore: ###if team1 is home
			# print("team1 is home")
			if int(row[3]) == VScore:
				# print("team2 is visitor")
				team1Score = HScore
				team2Score = VScore
				team1Home = 1
			
		elif int(row[2]) == VScore: #### if team1 is visitor
			# print("team1 is visitor")
			if int(row[3]) == HScore:
				# print("team2 is home")
				team1Score = VScore
				team2Score = HScore
				team2Home = 1
		else:
			print("possible game mismatch. score did not match either team")

		if team1Score > team2Score:
			currentRow.append(1)
		else:
			currentRow.append(0)
		currentRow.append(team1Score)
		currentRow.append(team2Score)
		currentRow.append(team1Home)
		for i in range(5,707):
			currentRow.append(row[i])
		currentRow.append(team2Home)
		for i in range(708,len(row)):
			currentRow.append(row[i])

		writerTrain.writerow(currentRow)
	except:
		try:
			# print("no clear Home/Visitor - " + row[0])
			team1Home = 0.5
			team2Home = 0.5
			team1Score = int(row[2])
			team2Score = int(row[3])
			if team1Score > team2Score:
				currentRow.append(1)
			else:
				currentRow.append(0)
			currentRow.append(team1Score)
			currentRow.append(team2Score)
			currentRow.append(team1Home)
			for i in range(5,707):
				currentRow.append(row[i])
			currentRow.append(team2Home)
			for i in range(708,len(row)):
				currentRow.append(row[i])

			writerTrain.writerow(currentRow)
		except:
			print("this game is just weird")


