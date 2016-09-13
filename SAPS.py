import time, datetime, math, random
import HalcyonNHLdb


class SAPS():

	def __init__(self,season):
		self.stats_db = HalcyonNHLdb.HalcyonNHLdb()
		self.season = season
		self.coefficients = {}
		self.build_date = datetime.datetime.now()