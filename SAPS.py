import time, datetime, math, random
import numpy
import HalcyonNHLdb
from config import CONFIG as config


class SAPS():

	def __init__(self,season_string,saps_option):
		self.stats_db = HalcyonNHLdb.HalcyonNHLdb()
		self.season = season_string
		self.coefficients = {}
		self.build_date = datetime.datetime.now()
		self.saps_option = saps_option
		self.teams = config["teams"]
		self.num_teams = len(self.teams)

	def get_saps(self):

		if self.saps_option == 1:

			stats_mat = numpy.zeros(shape=(self.num_teams,20))
			team_counter = 0
			for team in self.teams:
				stats_mat[team_counter,0:7] = self.get_shot_stats_1(team)
				stats_mat[team_counter,7:14] = self.get_goal_stats_1(team)
				stats_mat[team_counter,14:20] = self.get_win_stats(team)
				defensive_stats = self.get_defensive_stats_1(team)
				team_counter +=1
			print stats_mat

	def get_win_stats(self,team):

		print "Team wins/losses: ", team
		wins_mat = numpy.zeros(6)

		# Get regulation wins and losses
		query_string = "SELECT COUNT(*) FROM Games{0} WHERE team=\'{1}\' AND result='W' AND gameType=\'RE\';".format(self.season,team)
		wins_mat[0] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) FROM Games{0} WHERE team=\'{1}\' AND result='L' AND gameType=\'RE\';".format(self.season,team)
		wins_mat[1] = int(self.stats_db.execute_num_query(query_string))
		# Get OT wins and losses
		query_string = "SELECT COUNT(*) FROM Games{0} WHERE team=\'{1}\' AND result='W' AND gameType=\'OT\';".format(self.season,team)
		wins_mat[2] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) FROM Games{0} WHERE team=\'{1}\' AND result='L' AND gameType=\'OT\';".format(self.season,team)
		wins_mat[3] = int(self.stats_db.execute_num_query(query_string))
		# Get SO wins and losses
		query_string = "SELECT COUNT(*) FROM Games{0} WHERE team=\'{1}\' AND result='W' AND gameType=\'SO\';".format(self.season,team)
		wins_mat[4] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) FROM Games{0} WHERE team=\'{1}\' AND result='L' AND gameType=\'SO\';".format(self.season,team)
		wins_mat[5] = int(self.stats_db.execute_num_query(query_string))


		print wins_mat
		return wins_mat

	def get_shot_stats_1(self,team):

		shots_mat = numpy.zeros(7)

		# Get regulation and OT SOG for score states from down 3 or more, down 2, etc, to up 3 or more
		query_string = "SELECT COUNT(*) shooter FROM Shots{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff<-2;".format(self.season,team)
		shots_mat[0] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Shots{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff=-2;".format(self.season,team)
		shots_mat[1] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Shots{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff=-1;".format(self.season,team)
		shots_mat[2] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Shots{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff=0;".format(self.season,team)
		shots_mat[3] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Shots{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff=1;".format(self.season,team)
		shots_mat[4] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Shots{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff=2;".format(self.season,team)
		shots_mat[5] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Shots{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff>2;".format(self.season,team)
		shots_mat[6] = int(self.stats_db.execute_num_query(query_string))

		return shots_mat

	def get_goal_stats_1(self,team):
		
		goals_mat = numpy.zeros(7)

		# Get regulation and OT goals for score states from down 3 or more, down 2, etc, to up 3 or more
		query_string = "SELECT COUNT(*) shooter FROM Goals{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff<-2;".format(self.season,team)
		goals_mat[0] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Goals{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff=-2;".format(self.season,team)
		goals_mat[1] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Goals{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff=-1;".format(self.season,team)
		goals_mat[2] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Goals{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff=0;".format(self.season,team)
		goals_mat[3] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Goals{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff=1;".format(self.season,team)
		goals_mat[4] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Goals{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff=2;".format(self.season,team)
		goals_mat[5] = int(self.stats_db.execute_num_query(query_string))
		query_string = "SELECT COUNT(*) shooter FROM Goals{0} WHERE team=\'{1}\' AND period<5 AND scoreDiff>2;".format(self.season,team)
		goals_mat[6] = int(self.stats_db.execute_num_query(query_string))

		return goals_mat

	def get_defensive_stats_1(self,team):
		return



if __name__ == "__main__":

	# Initialize class with year on which you want to build SAPS
	saps = SAPS("20152016",1)
	saps.get_saps()