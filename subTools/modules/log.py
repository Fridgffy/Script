import os
import datetime



def log(message):
	try:
		with open('./sub.log', 'a+') as logfile:
			log_time = f"[ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ]"
			logfile.write(f'{log_time} {message}\n')
	except Exception as e:
		print('[ log Error ] log: ' + str(e))
