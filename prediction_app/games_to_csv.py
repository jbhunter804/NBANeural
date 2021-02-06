#!/usr/bin/python
import psycopg2
from config import config
import csv


# app = Flask(__name__, static_folder='./static')
# print("we're printing")
# app._static_folder = os.path.abspath("static")
# print (os.path.abspath(app._static_folder))

# Declare your table
# class GameTable(Table):
#     # game_id = Col('GameID')
#     day = Col('Day')
#     home_team = Col('Home')
#     home_ml = Col('True Home ML')
#     visit_team = Col('Visitor')
#     visit_ml = Col('True Visitor ML')

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


def get_games():
    """ query data from the games table """
    conn = None
    gameList = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT game_id, day, home_team, visit_team, home_pct, visit_pct, home_ml, visit_ml, home_current_ml, visit_current_ml FROM games2 ORDER BY day DESC")
        # print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            # print(row)
            #day, home team, current home, model home, visit team, current visit, model visit
            gameList.append(Game(row[1], row[2], row[8], row[6], row[3], row[9], row[7]))
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return gameList

# @app.route('/')
# def index():
#     gameList = get_games()
#     # table = GameTable(gameList)
#     # print(table.__html__())
#     return render_template('index.html', title='Predictions', rows=gameList)

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) 
    outFile = "public/predictionData.csv"
    oFile = open(outFile, "w")
    writer = csv.writer(oFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    # writer.writerow(['Day', 'Home', 'Market', 'Model', 'Visitor', 'Market', 'Model'])
    gameList = get_games()
    for game in gameList:
        curRow = [game.day,game.home_team,game.home_current_ml, game.home_ml,game.visit_team,game.visit_current_ml,game.visit_ml]
        writer.writerow(curRow)
    oFile.close()

