#!/usr/bin/python
#import psycopg2
from flask import Flask, render_template
from config import config
from flask_table import Table, Col
from firebase_admin import credentials, firestore, initialize_app
import os
import csv

app = Flask(__name__, static_folder='./static')
# print("we're printing")
# app._static_folder = os.path.abspath("static")
# print (os.path.abspath(app._static_folder))

# Declare your table
class GameTable(Table):
    # game_id = Col('GameID')
    day = Col('Day')
    home_team = Col('Home')
    home_ml = Col('True Home ML')
    visit_team = Col('Visitor')
    visit_ml = Col('True Visitor ML')

# Get some objects
class Game(object):
    def __init__(self, day, home_team, home_current_ml, home_ml, visit_team, visit_current_ml, visit_ml):
        self.day = day
        self.home_team = home_team
        self.home_current_ml = home_current_ml
        self.home_ml = home_ml
        self.visit_team = visit_team
        self.visit_current_ml = visit_current_ml
        self.visit_ml = visit_ml


# def get_games():
#     """ query data from the games table """
#     conn = None
#     gameList = []
#     try:
#         params = config()
#         conn = psycopg2.connect(**params)
#         cur = conn.cursor()
#         cur.execute("SELECT game_id, day, home_team, visit_team, home_pct, visit_pct, home_ml, visit_ml, home_current_ml, visit_current_ml FROM games ORDER BY game_id")
#         print("The number of parts: ", cur.rowcount)
#         row = cur.fetchone()

#         while row is not None:
#             # print(row)
#             #day, home team, current home, model home, visit team, current visit, model visit
#             gameList.append(Game(row[1], row[2], row[8], row[6], row[3], row[9], row[7]))
#             row = cur.fetchone()

#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#     return gameList

def get_games():
    inFile = "predictionData.csv"
    iFile = open(inFile, "r")
    reader = csv.reader(iFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    gameList = []
    for row in reader:
        gameList.append(row)
    return gameList

@app.route('/')
def index():
    gameList = get_games()
    # table = GameTable(gameList)
    # print(table.__html__())
    return render_template('index.html', title='Predictions', gameList=gameList)

if __name__ == "__main__":
    app.run(host="0.0.0.0")#, port=int(os.environ.get("PORT", 5000)))      

