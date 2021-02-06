#!/usr/bin/python
import py_ball
from nba_api.stats.endpoints import teamgamelog, playerdashboardbygeneralsplits, boxscoreadvancedv2, playerdashboardbylastngames, playerdashboardbyclutch, playerdashboardbyopponent, boxscoresummaryv2
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
from pytrends.request import TrendReq

# HEADERS = {'Connection': 'close',
#            'Host': 'stats.nba.com',
#            'Origin': 'http://stats.nba.com',
#            'Referer':'https://www.google.com/',
#            'Upgrade-Insecure-Requests': '1',
#            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1)' + \
#            ' AppleWebKit/537.36 (KHTML, like Gecko)' + \
#            ' Chrome/78.0.3904.87 Safari/537.36'}
#######################################
#try to hit the NBA server a million times
#######################################
PLAYERS_PER_TEAM = 6
name2ID = {'Hawks': '1610612737','Celtics': '1610612738','Nets': '1610612751','Hornets': '1610612766','Bulls': '1610612741','Cavaliers': '1610612739','Mavericks': '1610612742','Nuggets': '1610612743','Pistons': '1610612765','Warriors': '1610612744','Rockets': '1610612745','Pacers': '1610612754','Clippers': '1610612746','Lakers': '1610612747','Grizzlies': '1610612763','Heat': '1610612748','Bucks': '1610612749','Timberwolves': '1610612750','Pelicans': '1610612740','Knicks': '1610612752','Thunder': '1610612760','Magic': '1610612753','76ers': '1610612755','Suns': '1610612756','Trail Blazers': '1610612757','Kings': '1610612758','Spurs': '1610612759','Raptors': '1610612761','Jazz': '1610612762','Wizards': '1610612764'}
ID2name = {'1610612737':'Atlanta Hawks','1610612738':'Boston Celtics','1610612751':'Brooklyn Nets','1610612766':'Charlotte Hornets','1610612741':'Chicago Bulls','1610612739':'Cleveland Cavaliers','1610612742':'Dallas Mavericks','1610612743':'Denver Nuggets','1610612765':'Detroit Pistons','1610612744':'Golden State Warriors','1610612745':'Houston Rockets','1610612754':'Indiana Pacers','1610612746':'Los Angeles Clippers','1610612747':'Los Angeles Lakers','1610612763':'Memphis Grizzlies','1610612748':'Miami Heat','1610612749':'Milwaukee Bucks','1610612750':'Minnesota Timberwolves','1610612740':'New Orleans Pelicans','1610612752':'New York Knicks','1610612760':'Oklahoma City Thunder','1610612753':'Orlando Magic','1610612755':'Philadelphia 76ers','1610612756':'Phoenix Suns','1610612757':'Portland Trail Blazers','1610612758':'Sacramento Kings','1610612759':'San Antonio Spurs','1610612761':'Toronto Raptors','1610612762':'Utah Jazz','1610612764':'Washington Wizards'}
Mon2MM = {'DEC':12, 'NOV':11, 'OCT': 10, 'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9}
def randUserAgent():
	user_agent_list = [
	   #Chrome
	    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	    #Firefox
	    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
	    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
	    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
	    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
	    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
	    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
	    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
	    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
	]
	user_agent = random.choice(user_agent_list)
	#Set the headers 
	headers = {'Connection': 'close','Host': 'stats.nba.com','Origin': 'http://stats.nba.com','Upgrade-Insecure-Requests': '1'}
	headers.update( {'User-Agent' : user_agent} )
	headers = {'User-Agent' : user_agent}
	return headers

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)
    return proxies

def randProxy(proxies):
	proxy = random.choice(proxies)
	return proxy

def delayPing():
	delays = [1.5]
	delay = np.random.choice(delays)
	time.sleep(delay)

#['GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY', 'PLAYER_ID', 
#'PLAYER_NAME', 'START_POSITION', 'COMMENT', 'MIN', 'E_OFF_RATING', 
#'OFF_RATING', 'E_DEF_RATING', 'DEF_RATING', 'E_NET_RATING', 'NET_RATING', 
#'AST_PCT', 'AST_TOV', 'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 
#'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'USG_PCT', 
#'E_USG_PCT', 'E_PACE', 'PACE', 'PACE_PER40', 'POSS', 
#'PIE']
#################################################################################################
## filters out players that don't dress or are injured in order to avoid their stats #####
#################################################################################################
def idEligblePlayers(boxscorePlayers):
	answer = {}
	for i in range(len(boxscorePlayers['data'])):
		if boxscorePlayers['data'][i][7][0:2] != 'DN':
			#print(boxscorePlayers['data'][i][5])
			answer[boxscorePlayers['data'][i][4]] = boxscorePlayers['data'][i][1]
	print(answer)
	return answer
#########################################################################################################
#####################finds the game date for later use ##################################################
#########################################################################################################
def getGameDate(team1Gamelog, gameID):
	notfound = []
	for i in range(len(team1Gamelog)):
		if team1Gamelog[i][1] == gameID:
			return team1Gamelog[i][2]
	print("wrong season")
	return notfound
#########################################################################################################
#####################takes list of all players, looks up overall stats, appends teamID, returns list
#########################################################################################################
def overallBasePlayerData(players, gameDate, season):#, proxies):
	answer = {}
	for playerID in players:
		# headers = randUserAgent()
		# proxy = randProxy(proxies)
		rawPlayerData = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id= playerID, season= season, date_to_nullable= gameDate, measure_type_detailed= "Base", per_mode_detailed="PerGame")
		playerData = rawPlayerData.overall_player_dashboard.get_dict()
		answer[playerID] = playerData['data'][0][6:27]
		teamID = players[playerID]
		answer[playerID].append(teamID)
		# print(answer[playerID])
		# if len(answer) > 0:
		# 	break
		delayPing()
	return answer

#########################################################################################################
#####################takes list of all players, looks up overall stats, appends teamID, returns list
#########################################################################################################
def overallAdvPlayerData(playerIDs, gameDate, season):#, proxies):
	answer = {}
	for playerID in playerIDs:
		rawPlayerData = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id= playerID, season= season, date_to_nullable= gameDate, measure_type_detailed= "Advanced", per_mode_detailed="PerGame")
		playerData = rawPlayerData.overall_player_dashboard.get_dict()
		answer[playerID] = playerData['data'][0][6:39]
		# print(answer[playerID])

		delayPing()
	return answer

#########################################################################################################
######takes list of relevant playerIDs (team1 are first 8, team2 are second 8), looks up past 5 stats, 
###### returns dict of (playerID, past5) entries.
######
#########################################################################################################
def past10gamesPlayerData(playerIDs, gameDate, season, BasePlayerData):
	answerCur10 = {}
	answerPast10 = {}
	for playerID in playerIDs:
		rawPlayerData = playerdashboardbylastngames.PlayerDashboardByLastNGames(player_id= playerID, season= season, date_to_nullable= gameDate, measure_type_detailed= "Base", per_mode_detailed="PerGame")#
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
######takes list of relevant playerIDs (team1 are first 8, team2 are second 8), looks up past 5 stats, 
###### returns dict of (playerID, past5) entries.
######
#########################################################################################################
def clutchPlayerData(playerIDs, gameDate, season, BasePlayerData):
	answer3Min = {}
	answer30Sec = {}
	for playerID in playerIDs:
		rawPlayerData = playerdashboardbyclutch.PlayerDashboardByClutch(player_id= playerID, season= season, date_to_nullable= gameDate, measure_type_detailed= "Base")
		playerData3Min = rawPlayerData.data_sets[2].get_dict() #Last3Min5PointPlayerDashboard
		try:
			answer3Min[playerID] = playerData3Min['data'][0][6:27]
		except:
			answer3Min[playerID] = BasePlayerData[playerID][:-1]
			print("overall stats instead of clutch")
		delayPing()
	return answer3Min


#########################################################################################################
######takes list of relevant playerIDs (team1 are first 8, team2 are second 8), looks up past 5 stats, 
###### returns dict of (playerID, past5) entries.
######
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
######takes list of relevant playerIDs (team1 are first 8, team2 are second 8), looks up past 5 stats, 
###### returns dict of (playerID, past5) entries.
######
#########################################################################################################
# def opponentPlayerData(playerIDs, gameDate, season, team1ID, team2ID):
# 	answer = {}
# 	for i in range(2*PLAYERS_PER_TEAM):
# 		if i < PLAYERS_PER_TEAM:
# 			rawPlayerData = playerdashboardbyopponent.PlayerDashboardByOpponent(player_id= playerIDs[i], season= season, date_to_nullable= gameDate, measure_type_detailed= "Advanced", opponent_team_id= team2ID, per_mode_detailed="PerGame") 
# 			playerData = rawPlayerData.nba_response.get_dict()
# 			# playerData = rawPlayerData.data_sets[1].get_dict() #Opponent Player Dashboard
# 			print(playerData)
# 			# answer[playerID] = playerData['data'][0][6:39]

# 		# else
# 		# 	rawPlayerData = playerdashboardbyclutch.PlayerDashboardByClutch(player_id= playerIDs[i], season= season, date_to_nullable= gameDate, measure_type_detailed= "Advanced", opponent_team_id= team1ID) 
# 		# 	playerData = rawPlayerData.data_sets[2].get_dict() #Last3Min5PointPlayerDashboard
# 		# 	answer[playerID] = playerData['data'][0][6:39]
# 	return answer

#########################################################################################################
#####################take all players and return list of top 8 per team#####################
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
#####################take all players and return array of relevent player IDs (top 8 per team),###########
#####################return sortedOverallStats for Teams 1 and 2
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
#####################take all players and return array of relevent player IDs (top 8 per team),###########
#####################return sortedOverallStats for Teams 1 and 2
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
def getTrends(gameDate, teamID, ID2name= ID2name):
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
#####################take all players and return array of relevent player IDs (top 8 per team),###########
#####################return sortedOverallStats for Teams 1 and 2
#########################################################################################################

def makeGameData(gameID, season):
	answer = []
	### find box score to filter out non-participants ###
	curBoxScore = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=gameID)#, headers= headers)#, proxy= randomProxy)
	delayPing()
	boxscorePlayers = curBoxScore.player_stats.get_dict()
	boxscoreTeams = curBoxScore.team_stats.get_dict()
	### save team IDs for future use ###
	team1ID = boxscoreTeams['data'][0][1]
	team2ID = boxscoreTeams['data'][1][1]
	### get game date for future use ###
	curGamelog = teamgamelog.TeamGameLog(team_id= team1ID, season= season[0:4])#, headers= headers)#, proxy= randomProxy)
	delayPing()
	curGamelog = curGamelog.nba_response.get_dict()['resultSets'][0]['rowSet']
	GameDate = getGameDate(curGamelog, gameID)
	### get game result in form of home team W and dict with each team's pts ###
	#### returns 1 for result if h wins, 0 if v wins. returns dict of team 1 with array of [score, boolean was home]
	gameResult, teamHV = teamData(gameID, team1ID, team2ID)
	### continuing to filter eligible players ###
	eligiblePlayers = idEligblePlayers(boxscorePlayers)
	### get basic data on eligible players ###
	curBasePlayerData = overallBasePlayerData(eligiblePlayers, GameDate, season)
	### get google trends data per hour for past 10 days. 100 is max value. putting this here to break up NBA Calls
	# team1Trends = getTrends(GameDate, team1ID)
	### filter out bench players ###
	playerIDs, BasePlayerData = filterBenchPlayers(curBasePlayerData, team1ID, team2ID)
	### create arrays with each team's players for future use
	team1PlayerIDs = playerIDs[:PLAYERS_PER_TEAM]
	team2PlayerIDs = playerIDs[PLAYERS_PER_TEAM:]
	### get player performance in current set of 10 games and past set. this will be weird due to 
	### current 10 being based on a variable amount of games, but is set to per game stats
	current10GameData, past10GameData = past10gamesPlayerData(playerIDs, GameDate, season, BasePlayerData)
	### get player clutch data
	player3MinData = clutchPlayerData(playerIDs, GameDate, season, BasePlayerData)
	### get overall advanced statistics on each player
	AdvPlayerData = overallAdvPlayerData(playerIDs, GameDate, season)

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
	return answer
#########################################################################################################
# gameID = "0021600442"
# season = '2016-17'
# testPlayerID = "202340"
#boxScoreTest#
# test = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=gameID)
# print(test.player_stats.get_dict())

# player # 
#test = commonplayerinfo.CommonPlayerInfo(player_id=2544)
#print(test.player_headline_stats.get_dict())

# headers = randUserAgent()
# proxies = get_proxies()
# randomProxy = randProxy(proxies)
################################################################################################
################################################################################################
# testBoxScore = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=gameID)#, headers= headers)#, proxy= randomProxy)
# delayPing()

# boxscorePlayers = testBoxScore.player_stats.get_dict()
# boxscoreTeams = testBoxScore.team_stats.get_dict()
# team1ID = boxscoreTeams['data'][0][1]
# team2ID = boxscoreTeams['data'][1][1]
# testGamelog = teamgamelog.TeamGameLog(team_id= team1ID, season= 2016)#, headers= headers)#, proxy= randomProxy)
# delayPing()
# testGamelog = testGamelog.nba_response.get_dict()['resultSets'][0]['rowSet']
# testGameDate = getGameDate(testGamelog, gameID)

# gameResult, teamHV = teamData(gameID, team1ID, team2ID)


# eligiblePlayers = idEligblePlayers(boxscorePlayers)
# testBasePlayerData = overallBasePlayerData(eligiblePlayers, testGameDate, season)#, proxies)
# playerIDs, BasePlayerData = filterBenchPlayers(testBasePlayerData, team1ID, team2ID)
# team1PlayerIDs = playerIDs[:PLAYERS_PER_TEAM]
# team2PlayerIDs = playerIDs[PLAYERS_PER_TEAM:]
# # print(len(playerIDs))
# # ################################################################################################
# current10GameData, past10GameData = past10gamesPlayerData(playerIDs, testGameDate, season)
# player3MinData = clutchPlayerData(playerIDs, testGameDate, season)
# AdvPlayerData = overallAdvPlayerData(playerIDs, testGameDate, season)

# print(current10GameData)
# print("\n")
# print(past10GameData)
# print("\n")
# print(player3MinData)
# print("\n")
# # print(player30SecData)

# print(getTrends(testGameDate, team1ID))

# gameData = makeGameData(gameID, season)
# print (gameData)


###inFile has meta data on where last cut off due to server issues. Will resume collecting there###
# inFile = "stoppingPlace.csv"
# iTrainFile = open(inFile, "r")
# readerTrain = csv.reader(iTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
# rows = []
# for row in readerTrain:
# 	rows.append(row)
# inFileNumber = int(rows[-1][0])
# inFileYear = int(rows[-1][1])
# inFileGame = int(rows[-1][2])
# iTrainFile.close()

# print(str(inFileNumber) + "  " + str(inFileYear) + "  " + str(inFileGame))

###outTrainFile is where each game's data will be written###
# outTrainFile = "testtrainData" + str(inFileNumber) + ".csv"
outTrainFile = "testtrain8Data.csv"
oTrainFile = open(outTrainFile, "w")
writerTrain = csv.writer(oTrainFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)



skippedGames = []
years = [15]#, 14, 13, 12]
for year in years:
	delayPing()
	###default is 165, so each team has >10 games for momentum stats###
	startGame = 1229#165
	endGame = 1230
	# if year == 16:
	# 	startGame = 789

	for game in range(startGame, endGame+1):
		curGameData = []
		skippedGame = ''

		try:
			gameIDstring = '002' + str(year) + str(game).zfill(5)
			season_string = '20'+ str(year) + '-' + str(year+1)
			skippedGame = gameIDstring
			gameData = makeGameData(gameIDstring, season_string)
			curGameData.append(gameIDstring)
			for d in gameData:
				curGameData.append(d)
			writerTrain.writerow(curGameData)
			print(gameIDstring + " successful")
			consecutiveMissed = 0
		except:
			skippedGame = gameIDstring
			skippedGames.append(skippedGame)
			print ("skipped " + gameIDstring)


oTrainFile.close()








