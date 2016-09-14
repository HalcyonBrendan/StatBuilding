import time, datetime, math, random
import HalcyonNHLdb


class SAPS():

	def __init__(self,season_string,saps_option):
		self.stats_db = HalcyonNHLdb.HalcyonNHLdb()
		self.season = season_string
		self.coefficients = {}
		self.build_date = datetime.datetime.now()
		self.saps_option = saps_option

	def get_saps(self):

		if saps_option == 1:
			shot_stats = self.get_shot_stats_1()
			goal_stats = self.get_goal_stats_1()
			defensive_stats = self.get_defensive_stats_1()


	def get_shot_stats_1(self):


	def get_goal_stats_1(self):


	def get_defensive_stats_1(self):



if __name__ == "__main__":

	# Initialize class with year on which you want to build SAPS
	saps = SAPS("20152016",1)