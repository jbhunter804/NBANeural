import csv
import random

# def BettingStrategy(payoffDict, curDayGames):


def uniformBettingStrategy(budget, payoffList, curDayGames):#, gameIndices):
	betSize = 100 #(.5 * budget) / curDayGames
	# gameIndices = range(len(payoffList))
	totalProfit = 0
	for i in range(curDayGames):
		
		curGame = random.choice(payoffList)
		# print(curGame)
		curPayoff = betSize * curGame
		payoffList.remove(curGame)
		curProfit = curPayoff - betSize
		totalProfit += curProfit
		# print("curProfit(" + str(curProfit) + ") = curPayoff(" + str(curPayoff) + ") - bet size (" + str(betSize) + ")")
	return totalProfit + budget, payoffList



gamesPerDay = range(3,12)

inFileName = "modelPayoffs.csv"
inFile = open(inFileName, "r")
reader = csv.reader(inFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outFileName = "mcUniform.csv"
outFile = open(outFileName, "w")
writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

payoffList = []
for row in reader:
	payoffList.append(float(row[0]))
# print(payoffList)
# gameIndices = range(len(payoffList))
for mc in range(10000):
	count = 0
	budget = 0
	totalGames = 0
	curPayoffList = payoffList.copy()
	while totalGames < 904 :
		curDayGames = random.choice(gamesPerDay)
		totalGames += curDayGames
		budget, curPayoffList = uniformBettingStrategy(budget, curPayoffList, curDayGames)#, gameIndices)
		# print(str(count) + " budget is " + str(budget) + ". games number today = " + str(curDayGames) + ". total games = " + str(totalGames))
		count += 1

	# print("broke loop")
	curDayGames = 915 - totalGames
	budget, curPayoffList = uniformBettingStrategy(budget, curPayoffList, curDayGames)#, gameIndices)
	# print("final " + str(budget))
	writer.writerow([budget])

