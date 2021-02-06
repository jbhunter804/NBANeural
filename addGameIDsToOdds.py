#!/usr/bin/python
import py_ball
from nba_api.stats.endpoints import teamgamelog
import csv
import time
import socket 
import requests
from datetime import datetime, timedelta, date
from lxml.html import fromstring
from torrequest import TorRequest
import urllib.request
import random
import requests
import numpy as np
import pandas as pd                        

ID2name = {'1610612737':'Atlanta Hawks','1610612738':'Boston Celtics','1610612751':'Brooklyn Nets','1610612766':'Charlotte Hornets','1610612741':'Chicago Bulls','1610612739':'Cleveland Cavaliers','1610612742':'Dallas Mavericks','1610612743':'Denver Nuggets','1610612765':'Detroit Pistons','1610612744':'Golden State Warriors','1610612745':'Houston Rockets','1610612754':'Indiana Pacers','1610612746':'Los Angeles Clippers','1610612747':'Los Angeles Lakers','1610612763':'Memphis Grizzlies','1610612748':'Miami Heat','1610612749':'Milwaukee Bucks','1610612750':'Minnesota Timberwolves','1610612740':'New Orleans Pelicans','1610612752':'New York Knicks','1610612760':'Oklahoma City Thunder','1610612753':'Orlando Magic','1610612755':'Philadelphia 76ers','1610612756':'Phoenix Suns','1610612757':'Portland Trail Blazers','1610612758':'Sacramento Kings','1610612759':'San Antonio Spurs','1610612761':'Toronto Raptors','1610612762':'Utah Jazz','1610612764':'Washington Wizards'}
Mon2MM = {'DEC':12, 'NOV':11, 'OCT': 10, 'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9}
odds2ID = {'Atlanta': '1610612737','Boston': '1610612738','Brooklyn': '1610612751','Charlotte': '1610612766','Chicago': '1610612741','Cleveland': '1610612739','Dallas': '1610612742','Denver': '1610612743','Detroit': '1610612765','GoldenState': '1610612744','Houston': '1610612745','Indiana': '1610612754','LAClippers': '1610612746','LALakers': '1610612747','Memphis': '1610612763','Miami': '1610612748','Milwaukee': '1610612749','Minnesota': '1610612750','NewOrleans': '1610612740','NewYork': '1610612752','OklahomaCity': '1610612760','Orlando': '1610612753','Philadelphia': '1610612755','Phoenix': '1610612756','Portland': '1610612757','Sacramento': '1610612758','SanAntonio': '1610612759','Toronto': '1610612761','Utah': '1610612762','Washington': '1610612764'}

def gameDate2Timeframe(gameDate, Mon2MM= Mon2MM):
	answer = ''
	year = int(gameDate[-4:])
	day = int(gameDate[-8:-6])
	mon = int(Mon2MM[gameDate[0:3]])
	answer = date(year, mon, day)

	return answer

def getGameID(team1Gamelog, relDate):
	notfound = "not found"
	for game in team1Gamelog:
		gameDate = game[2]
		gameDay = gameDate2Timeframe(gameDate)
		if relDate == gameDay:
			# print(relDate)
			return game[1]
	# print("wrong season")
	return notfound


for season in [2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009]:
	season = str(season)
	print("starting season" + season)
	inFile = "csvOdds/odds" + season + ".csv"
	iTrainFile = open(inFile, "r")
	readerTrain = csv.reader(iTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

	outTrainFile = "csvOdds/gameIDodds" + season + ".csv"
	oTrainFile = open(outTrainFile, "w")
	writerTrain = csv.writer(oTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

	allTeamGameLogs = {}
	for team in odds2ID:
		curGamelog = teamgamelog.TeamGameLog(team_id= odds2ID[team], season= season)#, headers= headers)#, proxy= randomProxy)
		curGamelog = curGamelog.nba_response.get_dict()['resultSets'][0]['rowSet']
		allTeamGameLogs[team] = curGamelog
		time.sleep(2)

	for row in readerTrain:
		currentRow = []
		if row[0] == 'Date':
			continue
		try:
			relGamelog = allTeamGameLogs[row[3]]
			dateInt = int(row[0])
			relDay = dateInt % 100
			relMon = int(dateInt / 100)
			seasonInt = int(season)
			if relMon < 10:
				seasonInt+= 1
			relDate = date(seasonInt, relMon, relDay)
			gameID = getGameID(relGamelog, relDate)
			currentRow.append(gameID)
			for i in [2,3,8, 9,10,11]:
				currentRow.append(row[i])
			if currentRow[0] != "not found":
				writerTrain.writerow(currentRow)
		except:
			continue
	iTrainFile.close()
	oTrainFile.close()
	print("ending season" + season)
# curGamelog = teamgamelog.TeamGameLog(team_id= teamID, season= season)#, headers= headers)#, proxy= randomProxy)
# curGamelog = curGamelog.nba_response.get_dict()['resultSets'][0]['rowSet']
# print(curGamelog)