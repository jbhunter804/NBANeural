from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import urllib.request
import random
import requests
import csv

name2ID = {'Hawks': '1610612737','Celtics': '1610612738','Nets': '1610612751','Hornets': '1610612766','Bulls': '1610612741','Cavaliers': '1610612739','Mavericks': '1610612742','Nuggets': '1610612743','Pistons': '1610612765','Warriors': '1610612744','Rockets': '1610612745','Pacers': '1610612754','Clippers': '1610612746','Lakers': '1610612747','Grizzlies': '1610612763','Heat': '1610612748','Bucks': '1610612749','Timberwolves': '1610612750','Pelicans': '1610612740','Knicks': '1610612752','Thunder': '1610612760','Magic': '1610612753','76ers': '1610612755','Suns': '1610612756','Trail Blazers': '1610612757', 'Trailblazers': '1610612757','Kings': '1610612758','Spurs': '1610612759','Raptors': '1610612761','Jazz': '1610612762','Wizards': '1610612764'}
ID2name = {'1610612737':'Atlanta Hawks','1610612738':'Boston Celtics','1610612751':'Brooklyn Nets','1610612766':'Charlotte Hornets','1610612741':'Chicago Bulls','1610612739':'Cleveland Cavaliers','1610612742':'Dallas Mavericks','1610612743':'Denver Nuggets','1610612765':'Detroit Pistons','1610612744':'Golden State Warriors','1610612745':'Houston Rockets','1610612754':'Indiana Pacers','1610612746':'Los Angeles Clippers','1610612747':'Los Angeles Lakers','1610612763':'Memphis Grizzlies','1610612748':'Miami Heat','1610612749':'Milwaukee Bucks','1610612750':'Minnesota Timberwolves','1610612740':'New Orleans Pelicans','1610612752':'New York Knicks','1610612760':'Oklahoma City Thunder','1610612753':'Orlando Magic','1610612755':'Philadelphia 76ers','1610612756':'Phoenix Suns','1610612757':'Portland Trail Blazers','1610612758':'Sacramento Kings','1610612759':'San Antonio Spurs','1610612761':'Toronto Raptors','1610612762':'Utah Jazz','1610612764':'Washington Wizards'}
Mon2MM = {'DEC':12, 'NOV':11, 'OCT': 10, 'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9}
ESPN2ID = {'Atlanta': '1610612737','Boston': '1610612738','Brooklyn': '1610612751','Charlotte': '1610612766','Chicago': '1610612741','Cleveland': '1610612739','Dallas': '1610612742','Denver': '1610612743','Detroit': '1610612765','Golden State': '1610612744','Houston': '1610612745','Indiana': '1610612754','LA': '1610612746','Los Angeles': '1610612747','Memphis': '1610612763','Miami': '1610612748','Milwaukee': '1610612749','Minnesota': '1610612750','New Orleans': '1610612740','New York': '1610612752','Oklahoma City': '1610612760','Orlando': '1610612753','Philadelphia': '1610612755','Phoenix': '1610612756','Portland': '1610612757','Sacramento': '1610612758','San Antonio': '1610612759','Toronto': '1610612761','Utah': '1610612762','Washington': '1610612764'}
now = datetime.now()
def espnTimeStringToMyTime(espnTime):
	date_time_obj = datetime.strptime(espnTime, '%Y-%m-%dT%H:%MZ')
	myDateTime = date_time_obj + timedelta(hours=9)
	return myDateTime

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
		myTime = espnTimeStringToMyTime(gameTime)
		allTimes.append(myTime)
	print(allTimes)
	lenAllTeams = len(allTeams)
	lenAllTimes = len(allTimes)
	dropTeams = lenAllTeams - (lenAllTimes * 2)
	allTeams =  allTeams[dropTeams:]
	for i in range(len(allTimes)):
		currentRow = []
		currentRow.append(allTeams[(2*i)+1]) # home
		currentRow.append(allTeams[2*i]) # visitor
		currentRow.append(allTimes[i]) # time
		answer.append(currentRow)
	# print(allTeams)
	return answer

def createNearGames(todayGames, now):
	answer = []
	for game in todayGames:
		timeToGame = (game[2] - now)
		minutesRemaining = timeToGame.total_seconds()/60
		if minutesRemaining < 30 and minutesRemaining > 27:
			answer.append(game)
	return answer

todayGames = createTodayGames()
# print(todayGames)
nearGames = createNearGames(todayGames, now)

outFile = "nearGames.csv"
oFile = open(outFile, "w")
writer = csv.writer(oFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


for row in nearGames:
	writer.writerow(row)

