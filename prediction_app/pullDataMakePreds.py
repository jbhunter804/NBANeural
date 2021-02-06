import os
import schedule
import time
from datetime import datetime, timedelta, date


def job():
	os.system('python3 findRunTime.py')
	file_size = os.path.getsize('nearGames.csv') 
	if file_size > 0:
		os.system('python3 pullUpcomingData.py')
		os.system('python3 combineTrainDataNewObs.py')
		os.system('python3 makePredictions.py')
		os.system('python3 predToDatabase.py')
		os.system('python3 games_to_csv.py')
		os.system('firebase deploy')
# schedule.every().day.at("20:53").do(job)

while 1:
    # schedule.run_pending()
    curHour = datetime.now().hour
    if curHour > 13:
    	print("back in an hour")
    	time.sleep(3600)
    job()
    time.sleep(180)