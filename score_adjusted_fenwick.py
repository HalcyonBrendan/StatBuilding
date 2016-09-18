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
				
				#print game_id[0], " game ", game_counter+1, " for ", team
				gid = game_id[0]

				game = Game.Game(self.season, gid, team)

				win_mat[team_counter,game_counter] = game.get_game_result()
				saf_mat[team_counter,game_counter] = self.compute_SAF(game)

				game_counter +=1

			print team
			print win_mat[team_counter]
			print saf_mat[team_counter]
			team_counter +=1


	# Includes pp, pk, and EN events for now
	def compute_SAF(self, game):

		fen_u2_avg = .44
		fen_u1_avg = .461
		fen_tied_avg = .50
		fen_d1_avg = .539
		fen_d2_avg = .56

		state_times = game.get_state_times()
		time_u2 = state_times[5]/60.
		time_u1 = state_times[4]/60.
		time_tied = state_times[3]/60.
		time_d1 = state_times[2]/60.
		time_d2 = state_times[1]/60.

		fen_events_by_state = game.get_rel_fen_by_state()
		fen_u2 = fen_events_by_state[5]
		fen_u1 = fen_events_by_state[4]
		fen_tied = fen_events_by_state[3]
		fen_d1 = fen_events_by_state[2]
		fen_d2 = fen_events_by_state[1]

		#print "times: ", time_u2, " ", time_u1, " ", time_tied, " ", time_d1, " ", time_d2
		#print "fens: ", fen_u2, " ", fen_u1, " ", fen_tied, " ", fen_d1, " ", fen_d2

		SAF = (time_u2*(fen_u2-fen_u2_avg)+time_u1*(fen_u1-fen_u1_avg)+time_tied*(fen_tied-fen_tied_avg)+time_d1*(fen_d1-fen_d1_avg)+time_d2*(fen_d2-fen_d2_avg))/(time_u2+time_u1+time_tied+time_d1+time_d2) + .5

		return SAF





if __name__ == "__main__":

	# Initialize class with year on which you want to build SAPS
	saf = SAF("20152016")
	saf.run_season()		


