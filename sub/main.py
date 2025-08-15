import sys
import os
import yaml
from modules import dataprocessing
from modules import runtools


# determine configuration file and configuration value
def judgement(path):
	try:
		# if config file exists
		if os.path.exists(path):
			with open(path,'r')as config_file:
				config = yaml.safe_load(config_file)
				dadaprocessing_config = config.get('dataprocessing')
				result = dadaprocessing_config.get('result')
				output = dadaprocessing_config.get('output')
				r_name = dadaprocessing_config.get('result_filename')

				# determine configuration value
				if result and output and r_name:
					if os.path.exists(result) and os.path.exists(output):
						name,extension = os.path.splitext(r_name)
						if extension == ".csv":
							return result,output,r_name
						else:
							print('[ Error ] The result file must be .csv')
							sys.exit(1)
					else:
						print('[ Error ] The result or output configuration value does not exist')
						sys.exit(1)
				else:
					print('[ Error ] Output/result must be configurd！')
					sys.exit(1)
		else:
			print('[ Error ] File config.yml does not exist')
			sys.exit(1)
	except Exception as e:
		print('[ Error ]  main.py -> judgement: ' + str(e))
		sys.exit(1)
def processing(result,result_file):
	try:
		alltools,allfiles = dataprocessing.main(result, result_file)
		total = len(alltools)
		if total == 14:
			print('[ Processing files ]')
			for file in allfiles:
				print(file)
		else:
			tlist = ['ESD', 'assetfinder', 'chaos', 'ctfr', 'dnsmap', 'fierce', 'findomain', 'github_subdomains', 'aquatone', 'ksubdomain', 'knock', 'subdomainbrute', 'subfinder', 'dnsub']
			elist = []
			for t in tlist:
				try:
					alltools.index(t)
				except Exception as e:
					if 'is not in list' in str(e):
						print(f'[ Error ] {t} an error occurred')
	except Exception as e:
		print('[ Error ] main.py -> processing: ' + str(e))

def runtool(result):
	try:
		runtools.main(result)
	except Exception as e:
		print('[ Error ] main.py -> runtool: ' + str(e))


if __name__ == '__main__':
	try:
		# get path configuration
		config_path = './config.yml'
		# judgement and get value
		result,output,r_name = judgement(config_path)
		result_file = os.path.join(output, r_name)

		# processing function
		processing(result,result_file)
		
		# runtools function 
		# runtools.main(result)
	except Exception as e:
		print('[ Error ] main.py -> main: ' + str(e))
		sys.exit(1)

