#!/usr/bin/python
import csv
import time
from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd
from pandas import read_csv
from matplotlib import pyplot as plt

def makeCumulativeRets(rets):
	cumRet = 0
	lenRets = len(rets)
	for i in range(lenRets):
		rets[i] += cumRet
		cumRet = rets[i]
	return rets

# dtypes = {
#     "Date": "datetime64",
#     "HomeTeam": "category",
#     "VisitTeam": "category",
#     "HomeMarketOdds": "int64",
#     "VisitMarketOdds": "int64",
#     "HomeModelOdds": "int64",
#     "VisitModelOdds": "int64",
#     "HomeScore": "int64",
#     "VisitScore": "int64",
#     "Payoff": "float64"
# }

# df = read_csv('currentSeasonResults.csv', usecols=list(dtypes), header=None, parse_dates=["Date"])
# print(df)


series = read_csv('currentSeasonResults.csv', header=None, parse_dates=True, squeeze=True)
series = series.rename({0: 'Date', 1:'HomeTeam', 2: 'VisitTeam', 3: 'HomeMarketOdds', 4: 'VisitMarketOdds', 5: 'HomeModelOdds', 6: 'VisitModelOdds', 7: 'HomeScore', 8: 'VisitScore', 9: 'Payoff'}, axis = 1)
rets = series['Payoff'] - 1
series['Returns'] = rets
rets = rets.rename({'Payoff': 'Return'})
cumRets = makeCumulativeRets(rets)
series['CumulativeReturn'] = cumRets

fig, ax = plt.subplots(figsize=(10, 6))

# Specify how our lines should look
ax.plot(series.Date, series.TotRet, color='tab:orange', label='Return')

# Same as above
ax.set_xlabel('Time')
ax.set_ylabel('Total Return')
ax.set_title('Model Performance')
ax.grid(True)
ax.legend(loc='upper left');
plt.show()
# inFile = "currentSeasonResults.csv"
# iFile = open(inFile, "r")
# reader = csv.reader(iFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
# data = []
# for row in reader:
# 	data.append(row)
# data = np.array(data)
# ####### data ordered from first bet to last in a numpy array ###############
# data = np.flip(data, axis=0)
