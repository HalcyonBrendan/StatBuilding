''' For each game in a specified season, compute the relative score-adjusted fenwick values.
	For now, formula computed to http://puckon.net/articles/improving-our-score-adjustment.php	
'''

import time, datetime, math, random
import numpy
import HalcyonNHLdb
from config import CONFIG as config


class SAC():

	def __init__(self, season_string):
		self.stats_db = HalcyonNHLdb.HalcyonNHLdb()
		self.season = season_string
		self.build_date = datetime.datetime.now()
		self.teams = config["teams"]
		self.num_teams = len(self.teams)

	def run_season(self):
		return

	def get_SAF(self, team, game_id):

		Fu2 = 

		SAF = (3.75*(Fu2-44)+8.46*(Fu1-46.1)+17.94*(Ftied-50)+8.46*(Fd1-53.9)+3.75*(Fd2-56))/42.36 + 50

		return