import time, datetime, math, random
import numpy
import HalcyonNHLdb
from config import CONFIG as config


class Game():

	def __init__(self, season_string, game_id, team):
		stats_db = HalcyonNHLdb.HalcyonNHLdb()

		query_string = "SELECT * FROM Shots{0} WHERE gameID={1} AND team=\'{2}\' ORDER BY eventID".format(season_string,game_id,team)
		self.team_shots_info = stats_db.execute_query(query_string)

		print team, " shots data: ", self.team_shots_info

		query_string = "SELECT * FROM Misses{0} WHERE gameID={1} AND team=\'{2}\' ORDER BY eventID".format(season_string,game_id,team)
		self.team_misses_info = stats_db.execute_query(query_string)

		query_string = "SELECT * FROM Shots{0} WHERE gameID={1} AND opponent=\'{2}\' ORDER BY eventID".format(season_string,game_id,team)
		self.opp_shots_info = stats_db.execute_query(query_string)

		query_string = "SELECT * FROM Misses{0} WHERE gameID={1} AND opponent=\'{2}\' ORDER BY eventID".format(season_string,game_id,team)
		self.opp_misses_info = stats_db.execute_query(query_string)



	def get_fenwick(self, team, game_id, score_diff):

		query_string = "SELECT COUNT(*) FROM Shots{0} WHERE gameID={1} AND team=\'{2}\' AND scoreDiff={3};".format(self.season,game_id,team,score_diff)
		print "Query: ", query_string
		try:
			num_shots = int(self.stats_db.execute_num_query(query_string))
		except:
			num_shots = 0

		query_string = "SELECT COUNT(*) FROM Misses{0} WHERE gameID={1} AND team=\'{2}\' AND scoreDiff={3};".format(self.season,game_id,team,score_diff)
		print "Query: ", query_string
		try:
			num_misses = int(self.stats_db.execute_num_query(query_string))
		except:
			num_misses = 0
		team_fen = num_shots+num_misses
		
		query_string = "SELECT COUNT(*) FROM Shots{0} WHERE gameID={1} AND opponent=\'{2}\' AND scoreDiff={3};".format(self.season,game_id,team,score_diff)
		print "Query: ", query_string
		try:
			num_shots = int(self.stats_db.execute_num_query(query_string))
		except:
			num_shots = 0
		query_string = "SELECT COUNT(*) FROM Misses{0} WHERE gameID={1} AND opponent=\'{2}\' AND scoreDiff={3};".format(self.season,game_id,team,score_diff)
		print "Query: ", query_string
		try:
			num_misses = int(self.stats_db.execute_num_query(query_string))
		except:
			num_misses = 0
		opp_fen = num_shots+num_misses

		if team_fen+opp_fen > 0:
			rel_fen = 100.*team_fen/(team_fen+opp_fen)
		else:
			rel_fen = -1
		return rel_fen

	def get_game_result(self, team, game_id):
		return 2