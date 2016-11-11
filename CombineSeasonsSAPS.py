''' Essentially just concatenates JSON files specified by a list of filepaths'''
import json

class CombineSAPS():

	def __init__(self,files,output_file):
		self.files = files
		self.output_file = output_file


	def concat_SAPS(self):
		
		data = []
		for file_path in SAPS_files:

			with open(file_path) as SAPS_file:    
				data.append(json.load(SAPS_file))

		SAPS_data = [game_SAPS for season_SAPS in data for game_SAPS in season_SAPS]
		#print SAPS_data
		self.print_json_file(SAPS_data)

	def print_json_file(self,json_object):

		json_file_name = "./outfiles/{0}.json".format(self.output_file)

		with open(json_file_name, 'w') as outfile:
			json.dump(json_object, outfile,sort_keys=True,indent=0,ensure_ascii=False)

		print "Successfully wrote combined SAPS JSON file to ", json_file_name


if __name__ == "__main__":

	out_name = "SAF_SAPS_1415_1516_a_0.json"
	SAPS_files = ["./outfiles/SAF_SAPS_20142015_alpha_0.json","./outfiles/SAF_SAPS_20152016_alpha_0.json"]
	combSAPS = CombineSAPS(SAPS_files,out_name)
	combSAPS.concat_SAPS()