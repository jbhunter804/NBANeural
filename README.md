# NBANeural
 Predicting NBA outcomes

 As a quarantine project, I decided to predict the outcome of NBA games and compare my model's win/loss probabilities to the win/loss probailities that betting markets' payoffs implied. 
 
 I chose the NBA, as opposed to other sports or basketball leagues, for a handful of reasons:
  1) Availability of data - stats.nba.com has great historical data by game/team/player
  2) Amount of players on the court - 10 players on the court allows for granular player-level data to be collected without ballooning in size.
  3) It's not baseball - I reasoned that the MLB would have many more data scientists analyzing the data and, therefore, a much more efficient market. 
  4) Near-parity of teams - all 30 teams in the NBA are at roughly the same ability level. This is not true in college basketball, where team and player talent is much more variable and much less predictable.

Data Collection - Key Choices:
 1) Player vs. Team Data - In order to get as granular as possible, I decided to gather data on the top 6 players by minutes on each team. I reasoned that players are not interchangeable and in order to create accurate predictions, the model needed to know who was in each starting lineup.
 2) Player Data: I included basic statistics, the NBA's "advanced" statistics, clutch statistics (how a player performs in the last 3 minutes of games that are within 3 points), and momentum statistics (how a player has done in the last 10 and 20 games)
 3) Betting Market Data: I included the market's implied probabilities in each observation as a starting point for the model to deviate from.
 
 Problems Arising from these Choices:
  1) Starting Lineups - While it is easy, in hidsight, to know which players featured prominently, it is much more difficult to forecast which six players will be on the court the longest. I decided to include the six players with the highest average minutes that are on a game's active roster. NBA teams are not required to cement their active/inactive rosters until 30 minutes before the game, so all analysis had to take place in this window.
  2) Limited Games for Training Data - There are 1230 games in a standard NBA season. Each team plays 82 games. In order to have the momentum data on the past 10-20 games, only games 20-82 could be included in the training data. I overcame this with a couple forms of data augmentation.
  3) Market Payoffs - Much like the concerns with the starting lineups, I needed to scrape the current market data right before inputting the data into the model.
 
 Data Augmentation:
 Using the past 6 seasons of NBA games, I turned each game into 24 different observations by both alternating the order of teams and the order of players within teams.
 
 Model Specs:
 I trained a neural network using Keras. The hyperparameter choices were a result of quite a bit of experimentation.
 
 Testing:
 Conducted in and out of sample tests. Used the abbreviated season in the "bubble" as the out of sample test.
 
 Performance (as of Feb 5):
 Went live on January 21. After just over 100 games, ROI is ~8%.
 
