import os
import datetime
from . import config_var



def log(message):
	try:
		o_path = config_var.o_path
		# determine if o_path exist
		if os.path.exists(o_path):
			log_pathname = o_path + 'sub.log'
			with open(log_pathname, 'a+') as logfile:
				log_time = f"[ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ]"
				logfile.write(f'{log_time} {message}')
		else:
			print('[ Error ] o_path in config_var.py is not exist')
			sys.exit(1)
	except Exception as e:
		print('[ Error ] log -> log: ' + str(e))

