import time, datetime, math, random
import numpy
import HalcyonNHLdb
from config import CONFIG as config


class Game():

	def __init__(self, season_string, game_id, team):
		stats_db = HalcyonNHLdb.HalcyonNHLdb()

		self.game_id = game_id
		self.team = team

		query_string = "SELECT winner,gameType FROM Games{0} WHERE gameID={1} AND team=\'{2}\';".format(season_string,self.game_id,self.team)
		self.outcome = stats_db.execute_query(query_string)
		self.gameType = self.outcome[0][1]
		self.result = 5
		if self.outcome[0][0] == self.team and self.gameType == "RE":
			self.result  = 1
		elif self.outcome[0][0] != self.team and self.gameType == "RE":
			self.result = 0
		elif self.outcome[0][0] != self.team and self.gameType == "OT":
			self.result = 2
		elif self.outcome[0][0] == self.team and self.gameType == "OT":
			self.result = 3
		elif self.outcome[0][0] != self.team and self.gameType == "SO":
			self.result = 4
		

		query_string = "SELECT eventID,gameID,shooter,team,opponent,period,time,state,strength,scoreDiff FROM Shots{0} WHERE gameID={1} AND period<4 AND distance<70 ORDER BY eventID;".format(season_string,self.game_id)
		self.shots = stats_db.execute_query(query_string)

		query_string = "SELECT eventID,gameID,shooter,team,opponent,period,time,state,strength,scoreDiff FROM Misses{0} WHERE gameID={1} AND period<4 AND distance<70 ORDER BY eventID;".format(season_string,self.game_id)
		self.misses = stats_db.execute_query(query_string)

		query_string = "SELECT eventID,gameID,shooter,team,opponent,period,time,state,strength,scoreDiff FROM Goals{0} WHERE gameID={1} AND period<4 AND distance<70 ORDER BY eventID;".format(season_string,self.game_id)
		self.goals = stats_db.execute_query(query_string)

		self.num_shots = len(self.shots)
		self.num_misses = len(self.misses)
		self.num_goals = len(self.goals)
		self.num_game_events = self.num_shots+self.num_misses+self.num_goals

		self.game_events = []
		self.merge_events()

		self.state_times = []
		self.team_events_by_state = []
		self.opp_events_by_state = []
		self.parse_game()


	# merges all fenwick events into a two lists of tuples ordered by eventID (time in game)
	# one list for "team", one for "opp"
	def merge_events(self):

		shot_counter = 0
		miss_counter = 0
		goal_counter = 0

		min_event_id = numpy.inf

		for i in range(0,self.num_game_events):

			# Determine next eventID for each event type
			if shot_counter < self.num_shots:	next_shot_id = self.shots[shot_counter][0]
			else:	next_shot_id = numpy.inf
			if miss_counter < self.num_misses:	next_miss_id = self.misses[miss_counter][0]
			else:	next_miss_id = numpy.inf
			if goal_counter < self.num_goals:	next_goal_id = self.goals[goal_counter][0]
			else:	next_goal_id = numpy.inf

			# Determine which event type has lowest ID
			min_id = min(next_shot_id,next_miss_id,next_goal_id)
			next_event = [next_shot_id,next_miss_id,next_goal_id].index(min_id)

			# Append event to new list of tuples and increment accordingly
			if next_event == 0:
				# temporarily add event type to each tuple
				temp_tuple = self.add_play_type(self.shots[shot_counter],'shot')
				self.game_events.append(temp_tuple)
				shot_counter += 1
			elif next_event == 1:
				temp_tuple = self.add_play_type(self.misses[miss_counter],'miss')
				self.game_events.append(temp_tuple)
				miss_counter += 1
			else:
				temp_tuple = self.add_play_type(self.goals[goal_counter],'goal')
				self.game_events.append(temp_tuple)
				goal_counter += 1


	def parse_game(self):

		start_state_time = 0
		end_state_time = 0
		start_state_period = 1
		end_state_period = 1
		self.state_times = numpy.zeros(7)
		self.team_events_by_state = numpy.zeros(7)
		self.opp_events_by_state = numpy.zeros(7)
		curr_state = 3


		for i in range(0,self.num_game_events):

			if self.game_events[i][3] == self.team:
				self.team_events_by_state[curr_state] += 1
				
				if self.game_events[i][-1]=='goal':
					end_state_time = self.game_events[i][6]
					end_state_period = self.game_events[i][5]

					self.state_times[curr_state] += 1200*(end_state_period-start_state_period)+(end_state_time-start_state_time)
					start_state_time = end_state_time
					start_state_period = end_state_period

					curr_state += 1
					curr_state = min(curr_state,6)
			else:
				self.opp_events_by_state[curr_state] += 1

				if self.game_events[i][-1]=='goal':
					end_state_time = self.game_events[i][6]
					end_state_period = self.game_events[i][5]

					self.state_times[curr_state] += 1200*(end_state_period-start_state_period)+(end_state_time-start_state_time)
					start_state_time = end_state_time
					start_state_period = end_state_period
					
					curr_state -= 1
					curr_state = max(curr_state,0)

		end_state_time = 1200
		end_state_period = 3
		self.state_times[curr_state] += 1200*(end_state_period-start_state_period)+(end_state_time-start_state_time)


	def add_play_type(self,orig_tuple,event_type):

		return orig_tuple+(event_type,)



	def get_rel_fen_by_state(self):

		rel_fen_by_state = numpy.zeros(len(self.team_events_by_state))

		for i in range(0,len(self.team_events_by_state)):
			if min(self.team_events_by_state[i],self.opp_events_by_state[i]) > 0:
				rel_fen_by_state[i] = self.team_events_by_state[i]/(self.team_events_by_state[i]+self.opp_events_by_state[i])
			elif self.team_events_by_state[i] > 0:
				rel_fen_by_state[i] = 1
			elif self.opp_events_by_state[i] > 0:
				rel_fen_by_state[i] = 0
			else:
				rel_fen_by_state[i] = 0

		return rel_fen_by_state

	def get_state_times(self):
		return self.state_times

	def get_game_result(self):
		return self.result



