import MySQLdb


class HalcyonNHLDB():

	def __init__(self):
		self.db = MySQLdb.connect(passwd=config["mysql"]["pw"],host="localhost",user="root",db="halcyonnhl")