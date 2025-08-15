import sys
import os
import yaml
from modules import dataprocessing, runtools, output


# determine configuration file and configuration value
def judgement(path):
	try:
		# if config file exists
		if os.path.exists(path):
			with open(path,'r')as config_file:
				config_dict = yaml.safe_load(config_file)
				config = config_dict.get('main')
				r_path = config.get('r_path')
				o_path = config.get('o_path')
				r_name = config.get('r_name')

				# determine configuration value
				if r_path and o_path and r_name:
					if os.path.exists(r_path) and os.path.exists(o_path):
						name,extension = os.path.splitext(r_name)
						if extension == ".csv":
							return r_path, o_path, r_name
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
		print('[ Error ]  main -> judgement: ' + str(e))
		sys.exit(1)

def runtool(result):
	try:
		runtools.main(result)
	except Exception as e:
		print('[ Error ] main -> runtool: ' + str(e))

def processing(r_path):
	try:
		alltools, allfiles, allvalue = dataprocessing.main(r_path)
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
		# return dict data
		return allvalue
	except Exception as e:
		print('[ Error ] main -> processing: ' + str(e))

def output_file(r_pathname,allvalue):
	# write in result file
	output.write_in(r_pathname,allvalue)

if __name__ == '__main__':
	try:
		# get path configuration
		config_path = './config/config.yml'
		# judgement and get configuration value
		'''
		r_path: result path
		o_path: output path
		r_name: result file name
		r_pathname: result path + filename

		'''
		r_path, o_path, r_name = judgement(config_path)
		r_pathname = os.path.join(o_path, r_name)

		# call module dataprocessing and deal with result data
		# runtools.main(result)
		
		# call module dataprocessing and deal with result data
		allvalue = processing(r_path)
		print(allvalue)
		# call module output
		# output_file(r_pathname,allvalue)

	except Exception as e:
		print('[ Error ] main -> main: ' + str(e))
		sys.exit(1)

