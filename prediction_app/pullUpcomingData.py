#!/usr/bin/python
import py_ball
from nba_api.stats.endpoints import teamgamelog, playerdashboardbygeneralsplits, boxscoreadvancedv2, playerdashboardbylastngames, playerdashboardbyclutch, playerdashboardbyopponent, boxscoresummaryv2, teamplayeronoffsummary, commonallplayers, commonplayerinfo
import csv
import time
import socket 
import requests
from datetime import datetime, timedelta, date
# from lxml.html import fromstring
# from torrequest import TorRequest
import urllib.request
import random
import requests
import numpy as np
import pandas as pd                        
# from pytrends.request import TrendReq
from bs4 import BeautifulSoup




PLAYERS_PER_TEAM = 6
name2ID = {'Hawks': '1610612737','Celtics': '1610612738','Nets': '1610612751','Hornets': '1610612766','Bulls': '1610612741','Cavaliers': '1610612739','Mavericks': '1610612742','Nuggets': '1610612743','Pistons': '1610612765','Warriors': '1610612744','Rockets': '1610612745','Pacers': '1610612754','Clippers': '1610612746','Lakers': '1610612747','Grizzlies': '1610612763','Heat': '1610612748','Bucks': '1610612749','Timberwolves': '1610612750','Pelicans': '1610612740','Knicks': '1610612752','Thunder': '1610612760','Magic': '1610612753','76ers': '1610612755','Suns': '1610612756','Trail Blazers': '1610612757', 'Trailblazers': '1610612757','Kings': '1610612758','Spurs': '1610612759','Raptors': '1610612761','Jazz': '1610612762','Wizards': '1610612764'}
ID2name = {'1610612737':'Atlanta Hawks','1610612738':'Boston Celtics','1610612751':'Brooklyn Nets','1610612766':'Charlotte Hornets','1610612741':'Chicago Bulls','1610612739':'Cleveland Cavaliers','1610612742':'Dallas Mavericks','1610612743':'Denver Nuggets','1610612765':'Detroit Pistons','1610612744':'Golden State Warriors','1610612745':'Houston Rockets','1610612754':'Indiana Pacers','1610612746':'Los Angeles Clippers','1610612747':'Los Angeles Lakers','1610612763':'Memphis Grizzlies','1610612748':'Miami Heat','1610612749':'Milwaukee Bucks','1610612750':'Minnesota Timberwolves','1610612740':'New Orleans Pelicans','1610612752':'New York Knicks','1610612760':'Oklahoma City Thunder','1610612753':'Orlando Magic','1610612755':'Philadelphia 76ers','1610612756':'Phoenix Suns','1610612757':'Portland Trail Blazers','1610612758':'Sacramento Kings','1610612759':'San Antonio Spurs','1610612761':'Toronto Raptors','1610612762':'Utah Jazz','1610612764':'Washington Wizards'}
Mon2MM = {'DEC':12, 'NOV':11, 'OCT': 10, 'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9}
ESPN2ID = {'Atlanta': '1610612737','Boston': '1610612738','Brooklyn': '1610612751','Charlotte': '1610612766','Chicago': '1610612741','Cleveland': '1610612739','Dallas': '1610612742','Denver': '1610612743','Detroit': '1610612765','Golden State': '1610612744','Houston': '1610612745','Indiana': '1610612754','LA': '1610612746','Los Angeles': '1610612747','Memphis': '1610612763','Miami': '1610612748','Milwaukee': '1610612749','Minnesota': '1610612750','New Orleans': '1610612740','New York': '1610612752','Oklahoma City': '1610612760','Orlando': '1610612753','Philadelphia': '1610612755','Phoenix': '1610612756','Portland': '1610612757','Sacramento': '1610612758','San Antonio': '1610612759','Toronto': '1610612761','Utah': '1610612762','Washington': '1610612764'}

#################################################################################################
## set delay between url requests #####
#################################################################################################
def delayPing():
	delays = [1.5]
	delay = np.random.choice(delays)
	time.sleep(delay)
#################################################################################################
## pulls current injuries from CBS #####
#################################################################################################
def createInjuredList():
	answer = []
	url = 'https://www.cbssports.com/nba/injuries/'

	response = requests.get(url)
	html_soup = BeautifulSoup(response.text, 'html.parser')
	type(html_soup)
	player_containers = html_soup.find_all('span', class_ = 'CellPlayerName--long')
	injuries = html_soup.find_all('td', style = " min-width: 200px; width: 40%;")
	for i in range(len(player_containers)):
		if(len(injuries[i].text) != 56):
			# print(player_containers[i].a.text)
			answer.append(player_containers[i].a.text)
		# else:
		# 	print("skipped Game Time Decision")
	# print(answer)
	return answer

#################################################################################################
## pulls current moneyLine from Bovada #####
#################################################################################################
def findCurrentMoneyLine():
	answer = []
	url = 'https://www.betnow.eu/sportsbook-info/basketball/nba'

	response = requests.get(url)
	html_soup = BeautifulSoup(response.text, 'html.parser')
	# print(response.text[:500])

	allTeams = html_soup.find_all('div', class_ = 'odd-info-teams')
	allOdds = html_soup.find_all('div', class_ = 'col-md-2 col-xs-3')
	teams = []
	odds = []
	for odd in allOdds:
		odds.append(odd.span.text[1:-1])
	for team in allTeams:
		teams.append(team.div.span.text[4:])
	print(teams)
	print(odds)
	for i in range(len(odds)):
		if len(odds[i]) > 2:
			currentRow = []
			currentRow.append(name2ID[teams[i]])
			currentRow.append(odds[i])
			answer.append(currentRow)
	return answer



#################################################################################################
## pulls tomorrow's games from ESPN and returns [homeTeam, visitingTeam, dateTime] #####
#################################################################################################
def createTodayGames():
	answer = []
	url = 'https://www.espn.com/nba/schedule'
	response = requests.get(url)
	html_soup = BeautifulSoup(response.text, 'html.parser')
	# print(html_soup)
	upcomingDays = html_soup.find_all('table', class_ = 'schedule has-team-logos align-left')
	times = []
	for upcomingDay in upcomingDays:
		# print(upcomingDay)
		curTimes = upcomingDay.find_all('td', attrs = {'data-behavior':'date_time'})
		if len(curTimes) > 0:
			times = curTimes
			# print("found next day")
			break
	# while len(times) == 0:
	# 	print("getting next day")
	# 	upcomingDay = html_soup.find('table', class_ = 'schedule has-team-logos align-left')
	# 	times = upcomingDay.find_all('td', attrs = {'data-behavior':'date_time'})
	teams = upcomingDay.find_all('a', class_ = 'team-name')

	allTeams = []
	allTimes = []

	for team in teams:
		curTeam = team.span.text
		allTeams.append(ESPN2ID[curTeam])
	for time in times:
		gameTime = time['data-date']
		allTimes.append(gameTime)
	for i in range(len(allTimes)):
		currentRow = []
		currentRow.append(allTeams[(2*i)+1]) # home
		currentRow.append(allTeams[2*i]) # visitor
		currentRow.append(allTimes[i]) # time
		answer.append(currentRow)
	# print(allTeams)
	return answer
	# # type(html_soup)
	# days = html_soup.find_all('h2', class_ = 'table-caption')
	# for day in days:
	# 	dayString = day.text
	# 	dayStringDD = dayString[-2:]
	# 	print(dayStringDD)
	# 	if dayStringDD == relDay:
			

	# day_containers = html_soup.find_all('table', class_ = 'schedule has-team-logos align-left')

	# for day in day_containers:
	# 	date = 
	# 	teams = day.find_all('a', class_ = 'team-name')
	# 	for team in teams:
	# 		print(team.span.text)


#################################################################################################
## set delay between url requests #####
#################################################################################################
def moneylineToImpliedProbability(moneyLine):
	answer = 0
	moneyLine = float(moneyLine)
	if moneyLine > 0:
		answer = 100 / (100 + moneyLine)
	else:
		answer = (-1 * moneyLine) / ((-1 * moneyLine)+100)
	return answer
#################################################################################################
## returns of all active players this year
#################################################################################################
def createPlayerDict():
	rawData = commonallplayers.CommonAllPlayers(is_only_current_season=1)
	# rawData = commonplayerinfo.CommonPlayerInfo()
	data = rawData.nba_response.get_dict()
	data = data["resultSets"]
	data = data[0]["rowSet"]
	playerDict = {}
	for row in data:
		playerID = row[0]
		playerFLname = row[2]
		teamID = row[7]
		teamName = row[9]
		playerDict[playerID] = [teamID,teamName, playerID, playerFLname]
	return playerDict

#################################################################################################
## takes dict of all active players and returns a dict of players by team
#################################################################################################
def createTeamPlayerDict(playerDict):
	# rawData = commonallplayers.CommonAllPlayers(is_only_current_season=1)
	# data = rawData.nba_response.get_dict()
	# data = data["resultSets"]
	# data = data[0]["rowSet"]
	# playerDict = {}
	# for row in data:
	# 	playerID = row[0]
	# 	playerFLname = row[2]
	# 	teamID = row[7]
	# 	teamName = row[9]
	# 	playerDict[playerID] = [teamID,teamName, playerID, playerFLname]
	teamPlayerDict = {}
	for teamName in name2ID:
		teamID = name2ID[teamName]
		teamPlayers = []
		for playerID in playerDict:
			curTeamID = str(playerDict[playerID][0])
			if teamID == curTeamID:
				curTeamName = playerDict[playerID][1]
				curPlayerID = str(playerDict[playerID][2])
				curPlayerName = playerDict[playerID][3]
				teamPlayers.append([curTeamID, curTeamName, curPlayerID, curPlayerName])
		teamPlayerDict[teamID] = teamPlayers
	return teamPlayerDict

#################################################################################################
## grabs the relevant teams' players #####
#################################################################################################
def findRelevantTeams(team1ID, team2ID, teamPlayerDict):
	team1PlayerList = teamPlayerDict[team1ID]
	team2PlayerList = teamPlayerDict[team2ID]
	return team1PlayerList, team2PlayerList

#################################################################################################
## filters out players that are injured in order to avoid their stats. returns dict of playerID:teamID #####
#################################################################################################
def idEligblePlayers(team1PlayerList, team2PlayerList):
	answer = {}
	team1ID = team1PlayerList[0][0]
	team2ID = team2PlayerList[0][0]
	# injuryFileName = "currentInjuries.csv"
	# injuryFile = open(injuryFileName, "r")
	# readerInjuries = csv.reader(injuryFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	playerInjuries = createInjuredList()
	for playerName in playerInjuries:
		# curPlayerName = player[0]
		for i in range(len(team1PlayerList)):
			dictName = team1PlayerList[i][3]
			if playerName == dictName:
				team1PlayerList[i][0] = 'Injured'
				print(playerName)
		for i in range(len(team2PlayerList)):
			dictName = team2PlayerList[i][3]
			if playerName == dictName:
				team2PlayerList[i][0] = 'Injured'
				print(playerName)

	for i in range(len(team1PlayerList)):
		if team1PlayerList[i][0] != 'Injured':
			answer[team1PlayerList[i][2]] = team1ID

	for i in range(len(team2PlayerList)):
		if team2PlayerList[i][0] != 'Injured':
			answer[team2PlayerList[i][2]] = team2ID

	return answer
#########################################################################################################
#################### finds the game date for later use ##################################################
#########################################################################################################
def getGameDate(team1Gamelog, gameID):
	notfound = []
	for i in range(len(team1Gamelog)):
		if team1Gamelog[i][1] == gameID:
			return team1Gamelog[i][2]
	print("wrong season")
	return notfound
#########################################################################################################
#####################takes list of all players, looks up basic stats, appends teamID, returns list
#########################################################################################################
def overallBasePlayerData(players):#, proxies):
	answer = {}
	for playerID in players:
		# headers = randUserAgent()
		# proxy = randProxy(proxies)
		try:
			rawPlayerData = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id= playerID, measure_type_detailed= "Base", per_mode_detailed="PerGame")#, season_type_playoffs= "Pre Season")
			playerData = rawPlayerData.overall_player_dashboard.get_dict()
			# print(playerData)
			answer[playerID] = playerData['data'][0][6:27]
			teamID = players[playerID]
			answer[playerID].append(teamID)
		except:
			print("no data for " + str(playerID))
		# print(answer[playerID])
		# if len(answer) > 0:
		# 	break
		delayPing()
	return answer

#########################################################################################################
#####################takes list of all players, looks up advanced stats, returns dict of player:[stats]
#########################################################################################################
def overallAdvPlayerData(playerIDs):#, proxies):
	answer = {}
	for playerID in playerIDs:
		rawPlayerData = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id= playerID, measure_type_detailed= "Advanced", per_mode_detailed="PerGame")#, season_type_playoffs= "Pre Season")
		playerData = rawPlayerData.overall_player_dashboard.get_dict()
		answer[playerID] = playerData['data'][0][6:39]
		# print(answer[playerID])

		delayPing()
	return answer

#########################################################################################################
######takes list of relevant playerIDs (team1 are first 6, team2 are second 6), tries to lookup stats in games 0-10, 
###### and games 10-20, then returns dicts of playerID: [past10] and playerID: [past10-20] entries. If the player hasn't been in 20 games,
###### uses overall stats instead
#########################################################################################################
def past10gamesPlayerData(playerIDs, BasePlayerData):
	answerCur10 = {}
	answerPast10 = {}
	for playerID in playerIDs:
		rawPlayerData = playerdashboardbylastngames.PlayerDashboardByLastNGames(player_id= playerID, measure_type_detailed= "Base", per_mode_detailed="PerGame")#, season_type_playoffs= "Pre Season")#
		playerData = rawPlayerData.data_sets[5].get_dict()
		answerCur10[playerID] = playerData['data'][-1][6:27]
		try:
			answerPast10[playerID] = playerData['data'][-2][6:27]
		except:
			answerPast10[playerID] = BasePlayerData[playerID][:-1]
			print("overall stats instead of mom")

		delayPing()
	return answerCur10, answerPast10

#########################################################################################################
######takes list of relevant playerIDs (team1 are first 8, team2 are second 8), looks up basic stats for
###### performance in close games, then returns dict of playerID: [clutchBasicData].
######
#########################################################################################################
def clutchPlayerData(playerIDs, BasePlayerData):
	answer3Min = {}
	answer30Sec = {}
	for playerID in playerIDs:
		rawPlayerData = playerdashboardbyclutch.PlayerDashboardByClutch(player_id= playerID, measure_type_detailed= "Base")#, season_type_playoffs= "Pre Season")
		playerData3Min = rawPlayerData.data_sets[2].get_dict() #Last3Min5PointPlayerDashboard
		try:
			answer3Min[playerID] = playerData3Min['data'][0][6:27]
		except:
			answer3Min[playerID] = BasePlayerData[playerID][:-1]
			print("overall stats instead of clutch")
		delayPing()
	return answer3Min


#########################################################################################################
######takes gameID and both team IDs, and returns result(homeWin?) and answer (a dict of teamID:[score,home?])
###### CAN CAUSE SERIOUS ISSUES AND NEEDS TO BE REWORKED IN NEXT VERSION
#########################################################################################################
def teamData(gameID, team1ID, team2ID):
	answer = {}
	result = 1
	rawBoxScore = boxscoresummaryv2.BoxScoreSummaryV2(game_id=gameID)
	delayPing()
	boxScore = rawBoxScore.data_sets[5].get_dict()
	teamVID = boxScore['data'][0][3]
	teamHID = boxScore['data'][1][3]
	# print(boxScore['data'])
	teamVScore = boxScore['data'][0][-1]
	# print(ID2name[str(teamVID)] + " are V and their score was " + str(teamVScore))
	teamHScore = boxScore['data'][1][-1]
	# print(ID2name[str(teamHID)] + " are H and their score was " + str(teamHScore))

	if teamVScore > teamHScore:
		result = 0
	if teamVID == team1ID:
		answer[team1ID] = [teamVScore,0]
		answer[team2ID] = [teamHScore,1]

	elif teamVID == team2ID:
		answer[team1ID] = [teamHScore,1]
		answer[team2ID] = [teamVScore,0]

	else:
		print("teamID issue")
	# delay = np.random.choice(delays)
	# time.sleep(delay)
	return result, answer

#########################################################################################################
#####################take all players and return list of top 6 per team by minutes #####################
#########################################################################################################
def sortPlayersByMin(players, players_per_team= PLAYERS_PER_TEAM):
	answer = {}
	maxMin = 100000
	for player in players:
		currentMax = 0
		currentMaxID = 0 
		for player in players:
			if players[player][0] > currentMax and players[player][0] < maxMin:
				currentMax = players[player][0]
				currentMaxID = player
		answer[currentMaxID] = players[currentMaxID]
		maxMin = currentMax
		if len(answer) >= PLAYERS_PER_TEAM:
			break
	return answer

#########################################################################################################
#####################take all players and return array of relevent player IDs ([playerID1-playerID6]),
#####################return sortedOverallStats (playerID: [stats] for both teams
#########################################################################################################
def filterBenchPlayers(allOverallPlayerData, team1ID, team2ID, players_per_team= PLAYERS_PER_TEAM):
	allTeam1Players = {}
	allTeam2Players = {}
	sortedPlayerStats = {}
	for playerID in allOverallPlayerData:
		if allOverallPlayerData[playerID][-1] == team1ID:
			allTeam1Players[playerID] = allOverallPlayerData[playerID]
		elif allOverallPlayerData[playerID][-1] == team2ID:
			allTeam2Players[playerID] = allOverallPlayerData[playerID]
		else:
			print("got a bad teamID")

	sortedTeam1Players = sortPlayersByMin(allTeam1Players)
	sortedTeam2Players = sortPlayersByMin(allTeam2Players)
	playerIDs = []
	for playerID in sortedTeam1Players:
		playerIDs.append(playerID)
		sortedPlayerStats[playerID] = sortedTeam1Players[playerID]
	for playerID in sortedTeam2Players:
		playerIDs.append(playerID)
		sortedPlayerStats[playerID] = sortedTeam2Players[playerID]
	return playerIDs, sortedPlayerStats
#########################################################################################################
#####################takes NBA's date format and converts it for google trends
#####################
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
##################### NOT CURRENTLY IN USE. NEED TO RUN SEPERATE PROGRAM AND APPEND TO OVERALL DATASET IN NEXT VERSION
#########################################################################################################
def getTrends(teamID, ID2name= ID2name):
	answer = {}
	yearE, monE, dayE = gameDate2Timeframe(gameDate)
	endDate = date(yearE, monE, dayE)
	startDate = endDate - timedelta(days= 11)
	yearS = startDate.year
	monS = startDate.month
	dayS = startDate.day

	teamName = ID2name[str(teamID)]
	pytrend = TrendReq()
	pytrend.build_payload(kw_list=[teamName])
	historicalInterest = pytrend.get_historical_interest(keywords=[teamName], year_start= yearS, month_start = monS, day_start = dayS, year_end= yearE, month_end= monE, day_end= dayE, sleep= 60)
	delayPing()
	historicalData = historicalInterest[teamName].values.tolist()
	historicalData = historicalData[-240:]
	answer[teamID] = historicalData
	del pytrend
	# interest_over_time_df = pytrend.interest_over_time(year_start= year - 1, month_start = mon, day_start = day, year_end= year, month_end= mon, day_end= day)
	# print(interest_over_time_df.head())
	# related_queries_dict = pytrend.related_queries()
	# print(related_queries_dict)
	# suggestions_dict = pytrend.suggestions(keyword= teamName)
	# print(suggestions_dict)
	return answer
#########################################################################################################
##################### METHOD THAT PRODUCES THE DATA FOR EACH GAME
##################### IT DOES NOT ADD THE MARKET'S PROBS, WHICH IS HANDLED BY combineDataAndOdds.py
#########################################################################################################

def makeGameData(homeTeamID,vistTeamID,hImpliedProb, vImpliedProb, teamPlayerDict):#(gameID, season):
	answer = []
	### find box score to filter out non-participants ###
	# curBoxScore = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=gameID)#, headers= headers)#, proxy= randomProxy)
	# delayPing()
	# boxscorePlayers = curBoxScore.player_stats.get_dict()
	# boxscoreTeams = curBoxScore.team_stats.get_dict()





	### save team IDs for future use ###
	team1ID = homeTeamID
	team2ID = vistTeamID

	team1PlayerList, team2PlayerList = findRelevantTeams(team1ID, team2ID, teamPlayerDict)
	### get game date for future use ###
	# curGamelog = teamgamelog.TeamGameLog(team_id= team1ID, season= season[0:4])#, headers= headers)#, proxy= randomProxy)
	# delayPing()
	# curGamelog = curGamelog.nba_response.get_dict()['resultSets'][0]['rowSet']
	# GameDate = getGameDate(curGamelog, gameID)
	### get game result in form of home team W and dict with each team's pts ###
	#### returns 1 for result if h wins, 0 if v wins. returns dict of team 1 with array of [score, boolean was home]
	# gameResult, teamHV = teamData(gameID, team1ID, team2ID)
	gameResult = 0.5
	teamHV = {team1ID:[100,1],team2ID:[100,0]}

	### continuing to filter eligible players ###
	eligiblePlayers = idEligblePlayers(team1PlayerList, team2PlayerList)
	### get basic data on eligible players ###
	curBasePlayerData = overallBasePlayerData(eligiblePlayers)
	### get google trends data per hour for past 10 days. 100 is max value. putting this here to break up NBA Calls
	# team1Trends = getTrends(GameDate, team1ID)
	### filter out bench players ###
	playerIDs, BasePlayerData = filterBenchPlayers(curBasePlayerData, team1ID, team2ID)
	### create arrays with each team's players for future use
	team1PlayerIDs = playerIDs[:PLAYERS_PER_TEAM]
	team2PlayerIDs = playerIDs[PLAYERS_PER_TEAM:]
	### get player performance in current set of 10 games and past set. this will be weird due to 
	### current 10 being based on a variable amount of games, but is set to per game stats
	current10GameData, past10GameData = past10gamesPlayerData(playerIDs, BasePlayerData)
	### get player clutch data
	player3MinData = clutchPlayerData(playerIDs, BasePlayerData)
	### get overall advanced statistics on each player
	AdvPlayerData = overallAdvPlayerData(playerIDs)

	# team2Trends = getTrends(GameDate, team2ID)

	### to store each team's data before the game
	team1Data = []
	team2Data = []
	### put home/visitor bool first #####
	team1Data.append(teamHV[team1ID][1])

	team2Data.append(teamHV[team2ID][1])
	#### then add trends data on each team #######
	# for t in team1Trends[team1ID]:
	# 	team1Data.append(t)
	# for t in team2Trends[team2ID]:
	# 	team2Data.append(t)
	#### then add player data #######
	for playerID in team1PlayerIDs:
		base = curBasePlayerData[playerID]
		for b in range(len(base)-1):
			team1Data.append(base[b])
		cur10 = current10GameData[playerID]
		for c1 in range(len(cur10)):
			team1Data.append(cur10[c1])		
		past10 = past10GameData[playerID]
		for p1 in range(len(past10)):
			team1Data.append(past10[p1])
		clutch = player3MinData[playerID]
		for cl in range(len(clutch)):
			team1Data.append(clutch[cl])
		adv = AdvPlayerData[playerID]
		for a in range(len(adv)):
			team1Data.append(adv[a])

	for playerID in team2PlayerIDs:
		base = curBasePlayerData[playerID]
		for b in range(len(base)-1):
			team2Data.append(base[b])
		cur10 = current10GameData[playerID]
		for c1 in range(len(cur10)):
			team2Data.append(cur10[c1])		
		past10 = past10GameData[playerID]
		for p1 in range(len(past10)):
			team2Data.append(past10[p1])
		clutch = player3MinData[playerID]
		for cl in range(len(clutch)):
			team2Data.append(clutch[cl])
		adv = AdvPlayerData[playerID]
		for a in range(len(adv)):
			team2Data.append(adv[a])
	#### add game outcome first (hWin, score team 1, score team 2, if )
	answer.append(gameResult)
	answer.append(teamHV[team1ID][0])
	answer.append(teamHV[team2ID][0])
	#####add team 1 inputs ######
	for t1 in team1Data:
		answer.append(t1)
	#####add team 2 inputs ######
	for t2 in team2Data:
		answer.append(t2)
	#####add current market implied probabilities #####
	answer.append(hImpliedProb)
	answer.append(vImpliedProb)

	return answer

###inFile has meta data on where last cut off due to server issues. Will resume collecting there###
#######outdated#########################################
# inFile = "upcomingGames.csv"
# iMatchupFile = open(inFile, "r")
# readerMatchups = csv.reader(iMatchupFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
##################################################################
date = datetime.today() - timedelta(hours=14, minutes=00)
# outTrainFile = "gameData" + date.strftime('%Y-%m-%d') + ".csv"
outTrainFile = "nextDataForModel.csv"
oTrainFile = open(outTrainFile, "w")
writerTrain = csv.writer(oTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

inFile = "nearGames.csv"
iFile = open(inFile, "r")
reader = csv.reader(iFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


# rawBoxScore = boxscoresummaryv2.BoxScoreSummaryV2(game_id='0021900165')

# createInjuredList()


playerDict = createPlayerDict()
teamPlayerDict = createTeamPlayerDict(playerDict)
# print(teamPlayerDict)
count = 0
todayGames = createTodayGames()
# print(todayGames)
todayMoneyLines = findCurrentMoneyLine()
fixedMoneyLines = []
for moneyLine in todayMoneyLines:
	curRow = []
	curRow.append(moneyLine[0]) #teamID
	curRow.append(moneylineToImpliedProbability(moneyLine[1]))
	fixedMoneyLines.append(curRow)
# print(fixedMoneyLines)
for row in reader:
	print(row)
	if row[0] == 'Home Team':
		count +=1
		continue
	homeTeamID = row[0]
	visitTeamID = row[1]
	# homeMoneyLine = float(row[2])
	# visitMoneyLine = float(row[3])
	# hImpliedProb = moneylineToImpliedProbability(homeMoneyLine)
	# vImpliedProb = moneylineToImpliedProbability(visitMoneyLine)
	hImpliedProb = 0.5
	vImpliedProb = 0.5
	for ml in fixedMoneyLines:
		if homeTeamID == ml[0]:
			hImpliedProb = ml[1]
		elif visitTeamID == ml[0]:
			vImpliedProb = ml[1]
	curGameData = []
	skippedGame = ''

	gameData = makeGameData(homeTeamID, visitTeamID, hImpliedProb, vImpliedProb, teamPlayerDict)
	curGameData.append(homeTeamID) ### only to keep consistent with training data which had gameID first
	for d in gameData:
		curGameData.append(d)
	writerTrain.writerow(curGameData)
	print("home team - "+ ID2name[homeTeamID] + " vs " + ID2name[visitTeamID] + " - visiting team was successful")


oTrainFile.close()




