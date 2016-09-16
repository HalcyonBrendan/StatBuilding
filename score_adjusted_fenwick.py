''' For each game in a specified season, compute the relative score-adjusted fenwick values.
	For now, formula computed to http://puckon.net/articles/improving-our-score-adjustment.php	
'''

import time, datetime, math, random
import numpy
import HalcyonNHLdb
from config import CONFIG as config


class SAF():

	def __init__(self, season_string):
		self.stats_db = HalcyonNHLdb.HalcyonNHLdb()
		self.season = season_string
		self.build_date = datetime.datetime.now()
		self.teams = config["teams"]
		self.num_teams = len(self.teams)

	def run_season(self):
		return

	def get_SAF(self, team, game_id):

		Fu2 = self.get_fenwick(team, game_id, 2)
		Fu1 = self.get_fenwick(team, game_id, 1)
		Ftied = self.get_fenwick(team, game_id, 0)
		Fd1 = self.get_fenwick(team, game_id, -1)
		Fd2 = self.get_fenwick(team, game_id, -2)

		print Fu2, " ", Fu1, " ", Ftied, " ", Fd1, " ", Fd2

		SAF = (3.75*(Fu2-44)+8.46*(Fu1-46.1)+17.94*(Ftied-50)+8.46*(Fd1-53.9)+3.75*(Fd2-56))/42.36 + 50

		print SAF

		return SAF

	def get_fenwick(self, team, game_id, score_state):

		query_string = "SELECT COUNT(*) FROM Shots{0} WHERE game_id={1} AND team=\'{2}\' AND score_state={3};".format(self.season,game_id,team,score_state)
		num_shots = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) FROM Misses{0} WHERE game_id={1} AND team=\'{2}\' AND score_state={3};".format(self.season,game_id,team,score_state)
		num_misses = int(self.stats_db.execute_num_query(query_string))
		team_fen = num_shots+num_misses
		query_string = "SELECT COUNT(*) FROM Shots{0} WHERE game_id={1} AND opponent=\'{2}\' AND score_state={3};".format(self.season,game_id,team,score_state)
		num_shots = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) FROM Misses{0} WHERE game_id={1} AND opponent=\'{2}\' AND score_state={3};".format(self.season,game_id,team,score_state)
		num_misses = int(self.stats_db.execute_num_query(query_string))
		opp_fen = num_shots+num_misses
		rel_fen = 100.*team_fen/(team_fen+opp_fen)
		return rel_fen




if __name__ == "__main__":

	# Initialize class with year on which you want to build SAPS
	saf = SAF("20152016",1)
	saps.get_saps()		