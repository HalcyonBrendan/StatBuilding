import MySQLdb
from config import CONFIG as config

class HalcyonNHLdb():

	def __init__(self):
		self.db = MySQLdb.connect(passwd=config["mysql"]["pw"],host="localhost",user="root",db="halcyonnhl")
		self.cursor = self.db.cursor()

	def execute_command(self, command_string):
		self.cursor.execute(command_string)
		self.db.commit()

	def execute_query(self, query_string):
		self.cursor.execute(query_string)
        sql_out = self.cursor.fetchall()
        return sql_out