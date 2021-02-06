#!/usr/bin/python
import py_ball
from nba_api.stats.endpoints import boxscoresummaryv2
import csv
import time
import socket 
import requests
from datetime import datetime, timedelta, date
from lxml.html import fromstring
import urllib.request
import random
import requests
import numpy as np
import pandas as pd                        


#######################################
#try to hit the NBA server a million times
#######################################
PLAYERS_PER_TEAM = 6
name2ID = {'Hawks': '1610612737','Celtics': '1610612738','Nets': '1610612751','Hornets': '1610612766','Bulls': '1610612741','Cavaliers': '1610612739','Mavericks': '1610612742','Nuggets': '1610612743','Pistons': '1610612765','Warriors': '1610612744','Rockets': '1610612745','Pacers': '1610612754','Clippers': '1610612746','Lakers': '1610612747','Grizzlies': '1610612763','Heat': '1610612748','Bucks': '1610612749','Timberwolves': '1610612750','Pelicans': '1610612740','Knicks': '1610612752','Thunder': '1610612760','Magic': '1610612753','76ers': '1610612755','Suns': '1610612756','Trail Blazers': '1610612757','Kings': '1610612758','Spurs': '1610612759','Raptors': '1610612761','Jazz': '1610612762','Wizards': '1610612764'}
ID2name = {'1610612737':'Atlanta Hawks','1610612738':'Boston Celtics','1610612751':'Brooklyn Nets','1610612766':'Charlotte Hornets','1610612741':'Chicago Bulls','1610612739':'Cleveland Cavaliers','1610612742':'Dallas Mavericks','1610612743':'Denver Nuggets','1610612765':'Detroit Pistons','1610612744':'Golden State Warriors','1610612745':'Houston Rockets','1610612754':'Indiana Pacers','1610612746':'Los Angeles Clippers','1610612747':'Los Angeles Lakers','1610612763':'Memphis Grizzlies','1610612748':'Miami Heat','1610612749':'Milwaukee Bucks','1610612750':'Minnesota Timberwolves','1610612740':'New Orleans Pelicans','1610612752':'New York Knicks','1610612760':'Oklahoma City Thunder','1610612753':'Orlando Magic','1610612755':'Philadelphia 76ers','1610612756':'Phoenix Suns','1610612757':'Portland Trail Blazers','1610612758':'Sacramento Kings','1610612759':'San Antonio Spurs','1610612761':'Toronto Raptors','1610612762':'Utah Jazz','1610612764':'Washington Wizards'}
fullname2ID = {'Atlanta Hawks': '1610612737','Boston Celtics': '1610612738','Brooklyn Nets': '1610612751','Charlotte Hornets': '1610612766','Chicago Bulls': '1610612741','Cleveland Cavaliers': '1610612739','Dallas Mavericks': '1610612742','Denver Nuggets': '1610612743','Detroit Pistons': '1610612765','Golden State Warriors': '1610612744','Houston Rockets': '1610612745','Indiana Pacers': '1610612754','Los Angeles Clippers': '1610612746','Los Angeles Lakers': '1610612747','Memphis Grizzlies': '1610612763','Miami Heat': '1610612748','Milwaukee Bucks': '1610612749','Minnesota Timberwolves': '1610612750','New Orleans Pelicans': '1610612740','New York Knicks': '1610612752','Oklahoma City Thunder': '1610612760','Orlando Magic': '1610612753','Philadelphia 76ers': '1610612755','Phoenix Suns': '1610612756','Portland Trail Blazers': '1610612757','Sacramento Kings': '1610612758','San Antonio Spurs': '1610612759','Toronto Raptors': '1610612761','Utah Jazz': '1610612762','Washington Wizards': '1610612764'}
Mon2MM = {'DEC':12, 'NOV':11, 'OCT': 10, 'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9}

def delayPing():
	delays = [1.5]
	delay = np.random.choice(delays)
	time.sleep(delay)

#########################################################################################################
#####################finds the game date for later use ##################################################
#########################################################################################################

def gameDate2Timeframe(gameDate, Mon2MM= Mon2MM):
	answer = ''
	year = int(gameDate[-4:])
	day = int(gameDate[-8:-6])
	mon = int(Mon2MM[gameDate[0:3]])
	# answer = year + '-' + mon + '-'+ day
	# return answer
	return year, mon, day

#########################################################################################################
#####################take all players and return array of relevent player IDs (top 8 per team),###########
#####################return sortedOverallStats for Teams 1 and 2
#########################################################################################################
#############################################

def makeGameData(gameID, season):
	answer = []
	### find box score to filter out non-participants ###
	curBoxScore = boxscoresummaryv2.BoxScoreSummaryV2(game_id=gameID)#, headers= headers)#, proxy= randomProxy)
	delayPing()
	allData = curBoxScore.nba_response.get_dict()
	relevantData = allData['resultSets'][5]['rowSet']

	### save team IDs for future use ###
	team1ID = relevantData[0][3]
	team2ID = relevantData[1][3]
	### gameDate ###
	gameDate = relevantData[0][0][:-9]
	### team1 and 2 scores ###
	team1Score = relevantData[0][-1]
	team2Score = relevantData[1][-1]
	answer.append(gameDate)
	answer.append(team1ID)
	answer.append(team2ID)
	answer.append(team1Score)
	answer.append(team2Score)
	return answer

def makePredictedGames():	
	answer = []
	inFile = "public/predictionData.csv"
	iFile = open(inFile, "r")
	reader = csv.reader(iFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	for game in reader:
		curGame = []
		try:
			gameDate = datetime.strptime(game[0],'%M/%d/%y')
		except:
			gameDate = datetime.strptime(game[0],'%Y-%M-%d')
		gameDateString = gameDate.strftime('%Y-%M-%d')
		homeTeamID = fullname2ID[game[1]]
		homeMarketOdds = game[2]
		homeModelOdds = game[3]
		visitTeamID = fullname2ID[game[4]]
		visitMarketOdds = game[5]
		visitModelOdds = game[6]
		curGame.append(gameDateString)
		curGame.append(homeTeamID)
		curGame.append(visitTeamID)
		curGame.append(homeMarketOdds)
		curGame.append(visitMarketOdds)
		curGame.append(homeModelOdds)
		curGame.append(visitModelOdds)
		answer.append(curGame)
	return answer

def makeAllGames():
	gameDict = {}
	consecutiveMistakes = 0
	for game in range(180, 1230):
		if consecutiveMistakes > 5:
			return gameDict
		curGameData = []
		skippedGame = ''
		try:
			gameIDstring = '00220' + str(game).zfill(5)
			season_string = '2020-21'
			gameData = makeGameData(gameIDstring, season_string)
			gameDict[gameIDstring] = gameData
			consecutiveMistakes = 0
		except:
			print("error at game " + gameIDstring)
			consecutiveMistakes += 1
	return gameDict

def matchGamesFromLists(allGames, predictedGames):
	answer = {}
	##### cycling through nexted for loop to match games from lists
	for aGame in allGames:
		curGame = []
		for pGame in predictedGames:

	##### if gameDays match #########
			if allGames[aGame][0] == pGame[0]:
	##### if team1 is home match #########
				if int(allGames[aGame][1]) == int(pGame[1]) and int(allGames[aGame][2]) == int(pGame[2]):
	##### if team1 is home match, append team1 score(home score) then team2 score #########
					pGame.append(allGames[aGame][-2])
					pGame.append(allGames[aGame][-1])
					answer[aGame] = pGame
					continue
	##### else if team2 is home match #########
				elif int(allGames[aGame][1]) == int(pGame[2]) and int(allGames[aGame][2]) == int(pGame[1]):
	##### if team1 is visitor match, append team2 score(home score) then team1 score #########
					pGame.append(allGames[aGame][-1])
					pGame.append(allGames[aGame][-2])
					answer[aGame] = pGame
					continue
	return answer

def makeOverallReturn(combinedGameDict):
	payoffList = []
	for game in combinedGameDict:
		team1Market = int(combinedGameDict[game][3])
		team2Market = int(combinedGameDict[game][4])
		team1Model = int(combinedGameDict[game][5])
		team2Model = int(combinedGameDict[game][6])
		team1Score = int(combinedGameDict[game][7])
		team2Score = int(combinedGameDict[game][8])
####### if team1 won ########
		if team1Score > team2Score:
####### if team1 had a higher market payoff than model, the model implied a higher win prob for team 1 ########
			if team1Market > team1Model:
				if team1Market > 0:
					payoffList.append((team1Market/100) + 1)
				else:
					payoffList.append((100/abs(team1Market))+1)
####### if team2 had a higher market payoff than model, the model implied a higher win prob for team 2 ########
			else:
				payoffList.append(0)
####### if team2 won ########
		elif team1Score < team2Score:
####### if team1 had a higher market payoff than model, the model implied a higher win prob for team 1 ########
			if team2Market > team2Model:
				if team2Market > 0:
					payoffList.append((team2Market/100) + 1)
				else:
					payoffList.append((100/abs(team2Market))+1)
####### if team2 had a higher market payoff than model, the model implied a higher win prob for team 2 ########
			else:
				payoffList.append(0)

	payoffList = np.array(payoffList)
	# print(payoffList)
	totalProfit = payoffList.sum() - len(payoffList)
	return totalProfit, payoffList

outTrainFile = "currentSeasonResults.csv"
oTrainFile = open(outTrainFile, "w")
writerTrain = csv.writer(oTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

allGames = makeAllGames()
predictedGames = makePredictedGames()

combinedGameDict = matchGamesFromLists(allGames, predictedGames)
##### combinedGames now have scores ########
totalProfit, payoffList = makeOverallReturn(combinedGameDict)
print(totalProfit)
# print(combinedGameDict)
count = 0

for entry in combinedGameDict:
	combinedGameDict[entry].append(payoffList[count])
	count += 1
	writerTrain.writerow(combinedGameDict[entry])

print(combinedGameDict)

oTrainFile.close()








