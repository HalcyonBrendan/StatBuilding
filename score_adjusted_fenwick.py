''' For each game in a specified season, compute the relative score-adjusted fenwick values.
	For now, formula computed to http://puckon.net/articles/improving-our-score-adjustment.php	
'''

import time, datetime, math, random
import numpy
import HalcyonNHLdb, Game
from config import CONFIG as config


class SAF():

	def __init__(self, season_string):
		self.stats_db = HalcyonNHLdb.HalcyonNHLdb()
		self.season = season_string
		self.build_date = datetime.datetime.now()
		self.teams = config["teams"]
		self.num_teams = len(self.teams)

	def run_season(self):

		saf_mat = numpy.zeros(shape=(self.num_teams,82))
		win_mat = numpy.zeros(shape=(self.num_teams,82))
		team_counter = 0
		for team in self.teams:
			query_string = "SELECT gameID FROM Games{0} WHERE team=\'{1}\' ORDER BY gameID".format(self.season,team)
			team_game_ids = self.stats_db.execute_query(query_string)

			game_counter = 0
			for game_id in team_game_ids:
				gid = game_id[0]

				game = Game.Game(self.season, gid, team)

				#win_mat[team_counter,game_counter] = self.get_game_result(team, gid)
				#saf_mat[team_counter,game_counter] = self.get_SAF(team, gid)

				game_counter +=1
				break

			team_counter +=1

			break
		

	def get_SAF(self, team, game_id):

		Fu2_avg = 44
		Fu1_avg = 46.1
		Ftied_avg = 50
		Fd1_avg = 53.9
		Fd2_avg = 56

		print team, " ", game_id
		Fu2 = self.get_fenwick(team, game_id, 2)
		print Fu2
		if Fu2 < 0:
			Fu2 = Fu2_avg
		Fu1 = self.get_fenwick(team, game_id, 1)
		print Fu1
		if Fu1 < 0:
			Fu1 = Fu1_avg
		Ftied = self.get_fenwick(team, game_id, 0)
		print Ftied
		if Ftied < 0:
			Ftied = Ftied_avg
		Fd1 = self.get_fenwick(team, game_id, -1)
		print Fd1
		if Fd1 < 0:
			Fd1 = Fd1_avg
		Fd2 = self.get_fenwick(team, game_id, -2)
		print Fd2
		if Fd2 < 0:
			Fd2 = Fd2_avg

		print Fu2, " ", Fu1, " ", Ftied, " ", Fd1, " ", Fd2

		SAF = (3.75*(Fu2-44)+8.46*(Fu1-46.1)+17.94*(Ftied-50)+8.46*(Fd1-53.9)+3.75*(Fd2-56))/42.36 + 50

		print SAF

		return SAF





if __name__ == "__main__":

	# Initialize class with year on which you want to build SAPS
	saf = SAF("20152016")
	saf.run_season()		


