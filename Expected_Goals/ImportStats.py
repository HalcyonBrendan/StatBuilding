import MySQLdb, re, time, sys, math, signal
from datetime import date, timedelta
import numpy as np
import pandas as pd
import HalcyonNHLdb


class TeamStats():

	def __init__(self, season, max_dist):
		self.db = HalcyonNHLdb.HalcyonNHLdb()
		self.max_dist = max_dist
		if season == "combined":
			self.stats, self.team_GPs = self.retrieve_combined_stats()
		else:
			self.season = int(season)


	def retrieve_stats(self):
		query = """SELECT A.team AS team, A.GF AS GF, B.GA AS GA, C.Wins AS Wins 
			FROM (SELECT team, COUNT(*) AS GF FROM Goals{0} WHERE period<5 AND zone=\'Off\' GROUP BY team) AS A 
			JOIN (SELECT opponent, COUNT(*) AS GA FROM Goals{0} WHERE period<5 AND zone=\'Off\' GROUP BY opponent) AS B ON A.team = B.opponent 
			JOIN (SELECT winner, COUNT(*) AS Wins FROM Games{0} WHERE winner=team GROUP BY winner) AS C ON A.team = C.winner 
			ORDER BY A.team""".format(self.season,self.max_dist)
		goal_stats = pd.read_sql(query,con=self.db.get_connection())
		query = """SELECT COUNT(*) FROM Games{0} WHERE team="MTL";""".format(self.season)
		team_GPs = int(self.db.execute_query(query)[0][0])
		return goal_stats, team_GPs
