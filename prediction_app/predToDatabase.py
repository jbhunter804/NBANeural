#!/usr/bin/python

import psycopg2
from config import config
from datetime import datetime, timedelta, date
import csv
import requests
from bs4 import BeautifulSoup


name2ID = {'Hawks': '1610612737','Celtics': '1610612738','Nets': '1610612751','Hornets': '1610612766','Bulls': '1610612741','Cavaliers': '1610612739','Mavericks': '1610612742','Nuggets': '1610612743','Pistons': '1610612765','Warriors': '1610612744','Rockets': '1610612745','Pacers': '1610612754','Clippers': '1610612746','Lakers': '1610612747','Grizzlies': '1610612763','Heat': '1610612748','Bucks': '1610612749','Timberwolves': '1610612750','Pelicans': '1610612740','Knicks': '1610612752','Thunder': '1610612760','Magic': '1610612753','76ers': '1610612755','Suns': '1610612756', 'Trailblazers': '1610612757', 'Trail Blazers': '1610612757','Kings': '1610612758','Spurs': '1610612759','Raptors': '1610612761','Jazz': '1610612762','Wizards': '1610612764'}
ID2name = {'1610612737':'Atlanta Hawks','1610612738':'Boston Celtics','1610612751':'Brooklyn Nets','1610612766':'Charlotte Hornets','1610612741':'Chicago Bulls','1610612739':'Cleveland Cavaliers','1610612742':'Dallas Mavericks','1610612743':'Denver Nuggets','1610612765':'Detroit Pistons','1610612744':'Golden State Warriors','1610612745':'Houston Rockets','1610612754':'Indiana Pacers','1610612746':'Los Angeles Clippers','1610612747':'Los Angeles Lakers','1610612763':'Memphis Grizzlies','1610612748':'Miami Heat','1610612749':'Milwaukee Bucks','1610612750':'Minnesota Timberwolves','1610612740':'New Orleans Pelicans','1610612752':'New York Knicks','1610612760':'Oklahoma City Thunder','1610612753':'Orlando Magic','1610612755':'Philadelphia 76ers','1610612756':'Phoenix Suns','1610612757':'Portland Trail Blazers','1610612758':'Sacramento Kings','1610612759':'San Antonio Spurs','1610612761':'Toronto Raptors','1610612762':'Utah Jazz','1610612764':'Washington Wizards'}
Mon2MM = {'DEC':12, 'NOV':11, 'OCT': 10, 'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9}
ESPN2ID = {'Atlanta': '1610612737','Boston': '1610612738','Brooklyn': '1610612751','Charlotte': '1610612766','Chicago': '1610612741','Cleveland': '1610612739','Dallas': '1610612742','Denver': '1610612743','Detroit': '1610612765','Golden State': '1610612744','Houston': '1610612745','Indiana': '1610612754','LA': '1610612746','Los Angeles': '1610612747','Memphis': '1610612763','Miami': '1610612748','Milwaukee': '1610612749','Minnesota': '1610612750','New Orleans': '1610612740','New York': '1610612752','Oklahoma City': '1610612760','Orlando': '1610612753','Philadelphia': '1610612755','Phoenix': '1610612756','Portland': '1610612757','Sacramento': '1610612758','San Antonio': '1610612759','Toronto': '1610612761','Utah': '1610612762','Washington': '1610612764'}

def prob2MoneyLine(impliedProb):
	answer = '100'
	if impliedProb == 1:
		impliedProb -= 0.01
	if impliedProb == 0:
		impliedProb+=0.01
	# print(impliedProb)
	if impliedProb > 0.5:
		answer = int(-100 * (impliedProb/(1-impliedProb)))
		answer = str(answer - (answer % 10))
	elif impliedProb < 0.5:
		answer = int(100* (1 - impliedProb)/impliedProb)
		answer = '+' + str(answer - (answer % 10)) # ((100 - probability)/(probability) * 100)
	
	return answer

#################################################################################################
## pulls current moneyLine from BetNow #####
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
	# print(teams)
	# print(odds)
	for i in range(len(odds)):
		if len(odds[i]) > 2:
			currentRow = []
			currentRow.append(name2ID[teams[i]])
			currentRow.append(odds[i])
			# print(currentRow)
			answer.append(currentRow)
	return answer

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
	print(len(allTeams))
	for i in range(int(len(allTeams)/2)):
		currentRow = []
		currentRow.append(allTeams[(2*i)+1]) # home
		currentRow.append(allTeams[2*i]) # visitor
		# currentRow.append(allTimes[i]) # time
		answer.append(currentRow)
	print(allTimes)
	print(allTeams)
	print(answer)
	return answer

def insert_prediction(game_id, day, home_team, visit_team, home_pct, visit_pct, home_ml, visit_ml, home_current_ml, visit_current_ml):
	""" insert a new vendor into the vendors table """
	sql = """INSERT INTO games2(game_id, day,home_team,visit_team,home_pct,visit_pct,home_ml,visit_ml, home_current_ml, visit_current_ml)
			 VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s) RETURNING game_id;"""
	# sql = """DELETE FROM games"""
	conn = None
	test_id = None
	try:
		# read database configuration
		params = config()
		# connect to the PostgreSQL database
		conn = psycopg2.connect(**params)
		# create a new cursor
		cur = conn.cursor()
		# execute the INSERT statement
		cur.execute(sql,(game_id, day,home_team,visit_team,home_pct,visit_pct,home_ml,visit_ml, home_current_ml, visit_current_ml))
		# get the generated id back
		test_id = cur.fetchone()[0]
		# commit the changes to the database
		conn.commit()
		# close communication with the database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

	return test_id

def clear_duplicates():

	sql = """WITH cte AS (
	  			SELECT day, home_team, 
	     			row_number() OVER(PARTITION BY day, home_team ORDER BY visit_team) AS rn
	  			FROM games
			)
				DELETE cte WHERE rn > 1;"""
	try:
		# read database configuration
		params = config()
		# connect to the PostgreSQL database
		conn = psycopg2.connect(**params)
		# create a new cursor
		cur = conn.cursor()
		# execute the INSERT statement
		cur.execute(sql)
		# get the generated id back
		test_id = cur.fetchone()[0]
		# commit the changes to the database
		conn.commit()
		# close communication with the database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

if __name__ == '__main__':
	# insert one vendor
	# insert_prediction(game_id, day, home_team, visit_team, home_pct, home_ml, visit_ml)
	date = datetime.today() - timedelta(hours=14, minutes=00)
	predictionFile = "todayPreds.csv"
	predFile = open(predictionFile, "r")
	readerPred = csv.reader(predFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	todayGames = createTodayGames()
	print(todayGames)
	todayMoneyLines = findCurrentMoneyLine()
	# print(todayMoneyLines)
	gameFile = "public/todayGames.csv"
	oGameFile = open(gameFile, "w")
	writerGame = csv.writer(oGameFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


	count = 0
	# print("here...")
	curRow = []
	for row in readerPred:
		count += 1
		game_id = datetime.today().strftime('%m%d') + str(datetime.now().hour)  + str(datetime.now().minute) + str(count)
		today = datetime.today()
		todayEST = today - timedelta(hours=14)
		gameDay = datetime(todayEST.year, todayEST.month, todayEST.day)
		home_team = ''
		visit_team = ''
		home_current_ml = ''
		visit_current_ml = ''
		home_pct = float(row[1])
		visit_pct = 1.03 - home_pct

		home_ml = prob2MoneyLine(home_pct)
		print("model home = " + str(home_ml))
		visit_ml = prob2MoneyLine(visit_pct)
		homeIDcsv = str(row[0])
		print("home id" + homeIDcsv)
		gameVisitID = ""
		for game in todayGames:
			gameHomeID = game[0]
			if homeIDcsv == gameHomeID:
				# print(homeIDcsv)
				home_team = ID2name[gameHomeID]
				gameVisitID = game[1]
				visit_team = ID2name[gameVisitID]
		for moneyLine in todayMoneyLines:
			if moneyLine[0] == homeIDcsv:
				home_current_ml = moneyLine[1]
			elif moneyLine[0] == gameVisitID:
				visit_current_ml = moneyLine[1]

		# print(home_current_ml)
		# print(visit_current_ml)

		# game_id = int(game_id)
		print(home_team + " with market = " + home_current_ml + " and model = " + home_ml + " VS. " + visit_team + " with market = " + visit_current_ml + " and model = " + visit_ml)
		test_id = insert_prediction(game_id, gameDay, home_team, visit_team, home_pct, visit_pct, home_ml, visit_ml, home_current_ml, visit_current_ml)
		print(test_id)
		curRow = [home_team, home_current_ml, home_ml, visit_team, visit_current_ml, visit_ml]
		# writerGame.writerow(curRow)
	oGameFile.close()






