import sys
import os
import yaml
from modules import Toolsdata, Runtools, output, log, sendemail
import argparse
import time
import datetime


# determine configuration file and configuration value
def judge_config_pathname(config_pathname):
	try:
		# if config file exists
		if os.path.exists(config_pathname):
			return True
		else:
			log.log('[ Initial Error ] File config.yml does not exist')
			sys.exit(1)
	except Exception as e:
		log.log('[ Main Error ]  judge_config_pathname: ' + str(e))
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
				root_path = config.get('root_path')
				subdict = config.get('subdict')

				git_api = config_dict.get('git_api')
				chaos_api = config_dict.get('chaos_api')
				# determine configuration value
				if r_path:
					if o_path:
						if r_name:
							if root_path:
								if subdict:
									if os.path.exists(subdict):
										if os.path.exists(root_path):
											if os.path.exists(r_path) and os.path.exists(o_path):
												name,extension = os.path.splitext(r_name)
												if extension == ".csv":
													return r_path, o_path, r_name, root_path, git_api, chaos_api, subdict
												else:
													log.log('[ Config Error ] r_name value wrong, extension must be .csv')
													sys.exit(1)
											else:
												log.log('[ Config Error ] r_path or o_path value wrong')
												sys.exit(1)
										else:
											log.log('[ Config Error ] root_path value wrong')
											sys.exit(1)
									else:
										log.log('[ Config Error ] subdict value wrong')
										sys.exit(1)
								else:
									log.log('[ Config Error ] subdict value in config.yml does not exist')
									sys.exit(1)
							else:
								log.log('[ Config Error ] root_path value in config.yml does not exist')
								sys.exit(1)
						else:
							log.log('[ Config Error ] r_name value in config.yml does not exist')
							sys.exit(1)
					else:
						log.log('[ Config Error ] o_path value in config.yml does not exist')
						sys.exit(1)
				else:
					log.log('[ Config Error ] r_path value in config.yml does not exist')
					sys.exit(1)
	except Exception as e:
		log.log('[ Main Error ]  main_config_value: ' + str(e))
		sys.exit(1)

# get configuration -> Runtools
def runtools_config_value(config_pathname):
	try:
		with open(config_pathname,'r') as config_file:
			config_dict = yaml.safe_load(config_file)
			config = config_dict.get('Runtools')
			timeout = config.get('timeout')

			# determine configuration value
			if timeout:
				return timeout
			else:
				log.log('[ Config Error ] "timeout" must be configurd！')
				sys.exit(1)
	except Exception as e:
		log.log('[ Main Error ]  runtools_config_value: ' + str(e))
		sys.exit(1)

# get configuration -> sendemail
def sendemail_config_value(config_pathname):
	try:
		with open(config_pathname, 'r') as config_file:
			config_dict = yaml.safe_load(config_file)
			config = config_dict.get('E-mail')
			sender = config.get('sender')
			password = config.get('password')
			receiver = config.get('receiver')
			smtp_server = config.get('smtp_server')
			smtp_port = config.get('smtp_port')

			if sender and password and receiver and smtp_server and smtp_port:
				return sender, password, receiver, smtp_server, smtp_port
			else:
				log.log('[ Config Error ] E-mail configuration values does not exist')
				sys.exit(1)
	except Exception as e:
		log.log('[ Main Error ] sendemail_config_value: ' + str(e))
		sys.exit(1)
	
# call module Toolsdata and deal with result data
def Runtool(timeout, r_path, o_path, root_path, target, git_api, chaos_api, subdict):
	try:
		# if result dir not empty
		if not os.listdir(r_path):
			
			Runtools.main(timeout, r_path, o_path, root_path, target, git_api, chaos_api, subdict)
		else:
			log.log('[ Initial Error ] result dir is not empty')
			sys.exit(1)
	except Exception as e:
		log.log('[ Main Error ] Runtool: ' + str(e))
		sys.exit(1)

# call module Toolsdata and deal with result data
def Toolsdataprocess(r_path):
	try:
		alltools, allfiles = Toolsdata.main(r_path)
		total = len(alltools)
		# determine all tools perform
		log.log(f'[ ToolResult ] A total of {total} tools were run, (should be 13)')
		# if total == 13:
			# print processed files
			# print('[ Processing files ]')
			# for file in allfiles:
			# 	print(file)
		
		tlist = ['ESD', 'assetfinder', 'chaos', 'dnsmap', 'fierce', 'findomain', 'github_subdomains', 'aquatone', 'ksubdomain', 'knock', 'subdomainbrute', 'subfinder', 'dnsub']
		# tlist = ['ESD', 'assetfinder', 'chaos', 'ctfr', 'dnsmap', 'fierce', 'findomain', 'github_subdomains', 'aquatone', 'ksubdomain', 'knock', 'subdomainbrute', 'subfinder', 'dnsub']
		elist = []
		for t in tlist:
			try:
				alltools.index(t)
			except Exception as e:
				if 'is not in list' in str(e):
					log.log(f'[Result file Error ] {t} result file not find')
	except Exception as e:
		log.log('[ Main Error ] Toolsdataprocess: ' + str(e))
		sys.exit(1)

def output_file(r_pathname):
	try:
		# write in result file
		output.write_in(r_pathname)
	except Exception as e:
		log.log('[ Main Error ] output_file: ' + str(e))
		sys.exit(1)

def send_email(start, end, spend, sender, password, receiver, smtp_server, smtp_port, attachments):
	try:
		sendemail.send(start, end, spend, sender, password, receiver, smtp_server, smtp_port, attachments)
	except Exception as e:
		log.log('[ Main Error ] send_email ' + str(e))
		sys.exit(1)

if __name__ == '__main__':
	try:
		# start time
		start = datetime.datetime.now()
		start_time = time.time()

		log.log(f'[ Project execution start ]')
		# get path configuration
		log.log(f'[ Determine config imformaion is correct ]')
		config_pathname = './configs/config.yml'
		judge_config_pathname(config_pathname)

		### output values
		# r_path: result path; o_path: output path; r_name: result file name; r_pathname: result path + filename; root_path: project absolute path
		r_path, o_path, r_name, root_path, git_api, chaos_api, subdict = main_config_value(config_pathname)
		r_pathname = os.path.join(o_path, r_name)

		### Runtools values
		timeout = runtools_config_value(config_pathname)

		### email values
		sender, password, receiver, smtp_server, smtp_port = sendemail_config_value(config_pathname)
		attachments = [r_pathname, os.path.join(o_path, 'oneforall.csv')]

		### GET command line paramter
		parser = argparse.ArgumentParser()
		parser.add_argument('-t', '--target', dest='target', type=str, required=True, nargs=1, help='Target domain')
		args = parser.parse_args()
		target = args.target[0]

		### call module Runtools.py
		Runtool(timeout, r_path, o_path, root_path, target, git_api, chaos_api, subdict)
		
		### call module Toolsdata.py
		log.log('[ start Processing result file ]')
		Toolsdataprocess(r_path)

		### call module output.py
		log.log(f'[ Output result file: {r_pathname} ]')
		output_file(r_pathname)
		
		# end time
		end = datetime.datetime.now()
		end_time = time.time()

		spend = end_time - start_time

		### send email
		send_email(start, end, spend, sender, password, receiver, smtp_server, smtp_port, attachments)
		log.log(f'[ Email sending successfully: To {receiver}]')

		log.log('[ Project execution completed ]\n\n')
	except Exception as e:
		log.log('[ Main Error ] main: ' + str(e))
		sys.exit(1)




