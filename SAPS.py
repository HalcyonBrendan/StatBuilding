import time, datetime, math, random
import numpy
import HalcyonNHLdb
import Score_Adjusted_Fenwick as SAF
from config import CONFIG as config


class SAPS():

	def __init__(self,season_string,saps_option):
		self.stats_db = HalcyonNHLdb.HalcyonNHLdb()
		self.season = season_string
		self.build_date = datetime.datetime.now()
		self.saps_option = saps_option
		self.teams = config["teams"]
		self.num_teams = len(self.teams)

		self.saf = SAF.SAF(self.season)
		self.SAPS_mat = []

	def run_season(self):

		self.saf.run_season()

		saf_mat = self.saf.get_saf_matrix()
		win_mat = self.saf.get_win_matrix()
		self.SAPS_mat = numpy.zeros(shape=(self.num_teams,len(saf_mat[0])))

		team_counter = 0
		for team in self.teams:
			for game_counter in range(0,len(win_mat[team_counter])):

				result = win_mat[team_counter][game_counter]
				if result > 1:
					result = 0.5
			
				self.SAPS_mat[team_counter][game_counter] = self.build_SAPS(saf_mat[team_counter][game_counter],result) 

			print "Team: ", team
			print "Results: ", win_mat[team_counter]
			print "SAF: ", saf_mat[team_counter]
			print "SAPS: ", self.SAPS_mat[team_counter] 
			team_counter += 1


	def build_SAPS(self,game_SAF,game_result):

		alpha = 0.5

		game_SAPS = (1-alpha)*game_SAF + alpha*game_result

		return game_SAPS



if __name__ == "__main__":

	# Initialize class with year on which you want to build SAPS
	saps = SAPS("20152016",1)
	saps.run_season()