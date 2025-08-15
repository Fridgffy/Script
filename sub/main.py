import sys
import os
import yaml
from modules import Toolsdata, Runtools, output, log


# determine configuration file and configuration value
def judge_config_pathname(config_pathname):
	try:
		# if config file exists
		if os.path.exists(config_pathname):
			return True
		else:
			print('[ Error ] File config.yml does not exist')
			sys.exit(1)
	except Exception as e:
		print('[ Error ]  main -> judge_config_pathname: ' + str(e))
		sys.exit(1)

# get configuration -> main
def main_config_value(config_pathname):
	try:
		with open(config_pathname,'r')as config_file:
				config_dict = yaml.safe_load(config_file)
				config = config_dict.get('main')
				r_path = config.get('r_path')
				o_path = config.get('o_path')
				r_name = config.get('r_name')
				p_path = config.get('p_path')

				# determine configuration value
				if r_path and o_path and r_name and p_path:
					if os.path.exists(p_path):
						if os.path.exists(r_path) and os.path.exists(o_path):
							name,extension = os.path.splitext(r_name)
							if extension == ".csv":
								return r_path, o_path, r_name, p_path
							else:
								print('[ Error ] The result file must be .csv')
								sys.exit(1)
						else:
							print('[ Error ] The "result" or "output" configuration value does not exist')
							sys.exit(1)
					else:
						print('[ Error ] project absolute path dose not exist')
						sys.exit(1)
				else:
					print('[ Error ] config.yml value wrong')
					sys.exit(1)
	except Exception as e:
		print('[ Error ]  main -> main_config_value: ' + str(e))
		sys.exit(1)

# get configuration -> Runtools
def runtools_config_value(config_pathname):
	try:
		with open(config_pathname,'r')as config_file:
			config_dict = yaml.safe_load(config_file)
			config = config_dict.get('Runtools')

			interval = config.get('interval')

			# determine configuration value
			if interval:
				return interval
			else:
				print('[ Error ] "interval" must be configurd！')
				sys.exit(1)
	except Exception as e:
		print('[ Error ]  main -> main_config_value: ' + str(e))
		sys.exit(1)

# call module Toolsdata and deal with result data
def Runtool(interval, r_path, o_path, p_path, target):
	try:
		# if result dir not empty
		if not os.listdir(r_path):
			
			Runtools.main(interval, r_path, o_path, p_path, target)
		else:
			print('[ Error ] result dir is not empty')
			sys.exit(1)
	except Exception as e:
		print('[ Error ] main -> Runtool: ' + str(e))

# call module Toolsdata and deal with result data
def Toolsdataprocess(r_path):
	try:
		alltools, allfiles = Toolsdata.main(r_path)
		total = len(alltools)
		# determine all tools perform
		if total == 14:
			# print processed files
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
		print('[ Error ] main -> Toolsdataprocess: ' + str(e))

def output_file(r_pathname):
	try:
		# write in result file
		output.write_in(r_pathname)
	except Exception as e:
		print('[ Error ] main -> output_file: ' + str(e))

if __name__ == '__main__':
	try:
		# get path configuration
		config_pathname = './configs/config.yml'
		judge_config_pathname(config_pathname)

		### output value
		# r_path: result path; o_path: output path; r_name: result file name; r_pathname: result path + filename; p_path: project absolute path
		r_path, o_path, r_name, p_path = main_config_value(config_pathname)
		r_pathname = os.path.join(o_path, r_name)

		### tools value
		target = 'shisu.edu.cn'
		interval = runtools_config_value(config_pathname)
		Runtool(interval, r_path, o_path, p_path, target)
		#print(1)

		# Toolsdataprocess(r_path)

		# call module output
		# output_file(r_pathname)

	except Exception as e:
		print('[ Error ] main -> main: ' + str(e))
		sys.exit(1)


