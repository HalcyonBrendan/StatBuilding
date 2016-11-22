
import MySQLdb, re, time, sys, math, signal, json
from datetime import date, timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint



class ClusterPlots():

	def __init__(self,game_data):
		
		self.game_id = int(game_data["gameID"])
		self.x_stat = str(game_data["xStat"])
		self.y_stat = str(game_data["yStat"])

		#self.home = str(game_data["home"]["short"])
		#self.away = str(game_data["away"]["short"])

		self.home_centroid = game_data["home"]["stats"]
		self.away_centroid = game_data["away"]["stats"]

		training_games = game_data["trainingGames"]

		count = 0
		for game in training_games:
			if count == 0:
				training_df = pd.DataFrame([[game["gameID"], 0, game["away"]["closeTo"], game["away"]["stats"][0], game["away"]["stats"][1]]], columns=["gameID","isHome","closeTo","coord1","coord2"])
				training_df = training_df.append(pd.DataFrame([[game["gameID"], 1, game["home"]["closeTo"], game["home"]["stats"][0], game["home"]["stats"][1]]], columns=["gameID","isHome","closeTo","coord1","coord2"]))
			else:
				training_df = training_df.append(pd.DataFrame([[game["gameID"], 0, game["away"]["closeTo"], game["away"]["stats"][0], game["away"]["stats"][1]]], columns=["gameID","isHome","closeTo","coord1","coord2"]))
				training_df = training_df.append(pd.DataFrame([[game["gameID"], 1, game["home"]["closeTo"], game["home"]["stats"][0], game["home"]["stats"][1]]], columns=["gameID","isHome","closeTo","coord1","coord2"]))
			count += 1
		training_df = training_df.reset_index()
		del training_df["index"]
		self.training_df = training_df

		#print self.game_id
		#print self.x_stat, " ", self.y_stat
		#print self.home, " ", self.away
		#print "Away: ", self.away_centroid[0], " ", self.away_centroid[1]
		#print "Home: ", self.home_centroid[0], " ", self.home_centroid[1]
		#print self.training_df


	def build_plots(self,thresh):
		# Create new dataframes
		rel_df = pd.DataFrame(columns=self.training_df.columns)
		irrel_df = pd.DataFrame(columns=self.training_df.columns)

		# From training_df, select training pairs for which each "test" team has at least one of the pair within its thresh
		for i in range(0,len(self.training_df.index),2):
			gid = self.training_df["gameID"][i]
			temp_df = self.training_df.loc[self.training_df["gameID"] == gid]
			#print temp_df

			if temp_df.loc[i]["isHome"] == 1:
				print "Error"
				exit()
			else:
				x_dist = temp_df.loc[i]["coord1"] - self.away_centroid[0]
				y_dist = temp_df.loc[i]["coord2"] - self.away_centroid[1]
				away_away_dist = self.euclid_dist(x_dist,y_dist)
				x_dist = temp_df.loc[i]["coord1"] - self.home_centroid[0]
				y_dist = temp_df.loc[i]["coord2"] - self.home_centroid[1]
				away_home_dist = self.euclid_dist(x_dist,y_dist)
				#print away_away_dist, " ", away_home_dist

			if temp_df.loc[i+1]["isHome"] == 0:
				print "Error"
				exit()
			else:
				x_dist = temp_df.loc[i+1]["coord1"] - self.away_centroid[0]
				y_dist = temp_df.loc[i+1]["coord2"] - self.away_centroid[1]
				home_away_dist = self.euclid_dist(x_dist,y_dist)
				x_dist = temp_df.loc[i+1]["coord1"] - self.home_centroid[0]
				y_dist = temp_df.loc[i+1]["coord2"] - self.home_centroid[1]
				home_home_dist = self.euclid_dist(x_dist,y_dist)
				#print home_away_dist, " ", home_home_dist

			if away_away_dist < thresh and home_home_dist < thresh:
				rel_df = rel_df.append(temp_df,ignore_index =True)
			elif away_home_dist < thresh	and home_away_dist < thresh:
				rel_df = rel_df.append(temp_df,ignore_index =True)
			else:
				irrel_df = irrel_df.append(temp_df,ignore_index =True)

		self.plot_clusters(rel_df,irrel_df,thresh)


	def plot_clusters(self,rel_df,irrel_df,thresh):
		
		# 1) create plot and plot home and away test teams
		plt.figure()
		plt.plot(self.away_centroid[0],self.away_centroid[1],'ko',markersize=8)
		plt.plot(self.home_centroid[0],self.home_centroid[1],'kv',markersize=8)
		# 3) plot irrelevant training teams from irrel_df
		for i in range(0,len(irrel_df.index),2):
			x3 = [irrel_df.loc[i]["coord1"],irrel_df.loc[i+1]["coord1"]]
			y3 = [irrel_df.loc[i]["coord2"],irrel_df.loc[i+1]["coord2"]]
			plt.plot(x3,y3,marker='o',color=(.5,.5,.5),linewidth=0.2,alpha=0.2,markersize=1.5,markeredgewidth=0.1)
		# 2) plot relevant training teams from rel_df (with line connecting them)
		for i in range(0,len(rel_df.index),2):
			x2 = [rel_df.loc[i]["coord1"],rel_df.loc[i+1]["coord1"]]
			y2 = [rel_df.loc[i]["coord2"],rel_df.loc[i+1]["coord2"]]
			plt.plot(x2,y2,marker='o',color=(0,.593,0),linewidth=0.3,markersize=3,markeredgewidth=0.1)

		
		# 4) add details
		away_clust_area = plt.Circle((self.away_centroid[0], self.away_centroid[1]), radius=thresh, color='.7', alpha=.3)
		plt.gca().add_patch(away_clust_area)
		home_clust_area = plt.Circle((self.home_centroid[0], self.home_centroid[1]), radius=thresh, color='.3', alpha=.3)
		plt.gca().add_patch(home_clust_area)
		plt.xlim([-3.5,3.5])
		plt.ylim([-3.5,3.5])

		x_string = self.x_stat + " [Std Devs from Mean]"
		y_string = self.y_stat + " [Std Devs from Mean]"
		plt.xlabel(x_string)
		plt.ylabel(y_string)
		title_str = "Game " + str(self.game_id) + " Nearest Neighbours"
		plt.title(title_str)
		save_string = str(self.game_id) + "cluster_view_t" + str(thresh).replace('.','p') + ".png"
		print "Saving figure to: ", save_string
		plt.savefig(save_string,bbox_inches='tight',dpi=400)

	def euclid_dist(self,x_dist,y_dist):
		return np.sqrt(x_dist*x_dist + y_dist*y_dist)



def process_game_data(game_data_file):
	# Load game data from file
	filepath = "./Game_Files/" + game_data_file
	#print filepath
	with open(filepath) as data_file:
		gd = json.load(data_file)
	return(gd)

if __name__ == "__main__":

	# Set distance thresholds for "being member of cluster"
	thresholds = [.707,1.414]
	num_thresh = len(thresholds)

	game_data_file = sys.argv[1]
	pgd = process_game_data(game_data_file)
	cp = ClusterPlots(pgd)
	count = 0
	for thresh in thresholds:
		print "Generating plot for threshold ", count+1, " of ", num_thresh, ". Value: ", thresh
		bp = cp.build_plots(thresh)
		count += 1
	plt.show()
