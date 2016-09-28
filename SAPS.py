import time, datetime, math, random
import numpy, json
import matplotlib.pyplot as plt
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
		self.home_SAPS_array = []
		self.game_id_array = []

		# Set parameter [0,1] that determines bias towards game outcome
		self.alphas = [-0.1,-0.05,-0.01,0,0.01,0.025,0.05,0.1,0.25,0.5,0.75,1]

	def run_season(self):
		print "Computing SAPS for season ", self.season
		self.saf.run_season()

		saf_mat = self.saf.get_saf_matrix()
		win_mat = self.saf.get_win_matrix()
		game_id_mat = self.saf.get_game_id_matrix()
		is_home_mat = self.saf.get_is_home_matrix()

		query_string = "SELECT COUNT(*) FROM Games{0};".format(self.season)
		num_games = self.stats_db.execute_num_query(query_string)/2
		self.home_SAPS_array = numpy.zeros(num_games)
		self.game_id_array = numpy.zeros(num_games)

		for alpha in self.alphas:
			print "Computing SAPS with alpha = ", alpha
			SAPS_mat = numpy.zeros(shape=(self.num_teams,len(saf_mat[0])))
			team_counter = 0
			for team in self.teams:
				for game_counter in range(0,len(win_mat[team_counter])):
					gid = game_id_mat[team_counter,game_counter]
					result = win_mat[team_counter,game_counter]
					if result > 1:
						result = 0.5

					SAPS_mat[team_counter,game_counter] = self.build_SAPS(saf_mat[team_counter,game_counter],result,alpha) 

					if is_home_mat[team_counter,game_counter]:
						# Record SAPS of home team indexed by game id
						self.home_SAPS_array[int(gid%10000)-1] = SAPS_mat[team_counter,game_counter]
						self.game_id_array[int(gid%10000)-1] = int(gid)

				#print "Team: ", team
				#print "Results: ", win_mat[team_counter]
				#print "SAF: ", saf_mat[team_counter]
				#print "SAPS: ", SAPS_mat[team_counter]

				plot_flag = 0

				if plot_flag == 1:
					plt.figure(team_counter+1)
					games_x = numpy.arange(1,83)
					saps_y = SAPS_mat[team_counter]
					linear_fit = numpy.poly1d(numpy.polyfit(games_x,saps_y,1))
					fit_line = linear_fit(numpy.linspace(1,82,82))
					plt.plot(games_x,saps_y,'ro',games_x,fit_line,'b-')
					plt.title(team)
					plt.xlabel('Game Number')
					plt.ylabel('Rel. Score Adjusted Fenwick')
					plt.grid(True)
					plt.axis([1,82,0,1])

				team_counter += 1

			plt.show()
			self.build_SAPS_json(alpha)

	def build_SAPS(self,game_SAF,game_result,alpha):

		game_SAPS = (1-alpha)*game_SAF + alpha*game_result

		return game_SAPS

	def build_SAPS_json(self,alpha):
		SAPS_json_object = []
		for i in range(0,len(self.home_SAPS_array)):
			SAPS_json_object.append(
				{"gameID": int(self.game_id_array[i]), "home": self.home_SAPS_array[i]}
			)

		file_name = "SAF_SAPS_{0}_alpha_{1}".format(self.season,alpha)
		print_json_file(SAPS_json_object,file_name)

def print_json_file(json_object,file_name):

	json_file_name = "./outfiles/{0}.json".format(file_name)

	with open(json_file_name, 'w') as outfile:
		json.dump(json_object, outfile,sort_keys=True,indent=0,ensure_ascii=False)



if __name__ == "__main__":

	# Initialize class with year on which you want to build SAPS
	saps = SAPS("20152016",1)
	saps.run_season()