#! /usr/bin/env python

import os
import sys
import time
import subprocess


def start(shell_file, interval, r_path, o_path, p_path, shell_path, target):
	try:
		print(f'interval: {interval}')
#		shell_pathname = os.path.join(shell_path, shell_file)
		shell_pathname = 'ctfr -o /root/result/ctfr -d shisu.edu.cn > /root/workspace/output 2>&1'
		p = subprocess.Popen(shell_pathname, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if p.stderr.read():
			print(p.stderr.read())
		print(shell_pathname)
		print(p.stdout.read())
		returncode = p.wait()
		if returncode == 0:
			print('perform success')
		else:
			print(f"{p.returncode} perform error")
	except Exception as e:
		print('[ Error ] Runtools -> start: ' + str(e))
		sys.exit(1)











# main
def main(interval, r_path, o_path, p_path, target):
	try:
		shell_path = os.path.join(p_path, 'shells')
		for shell_file in os.listdir(shell_path):
			start(shell_file, interval, r_path, o_path, p_path, shell_path, target)
		# start function 
		# start(interval)
	except Exception as e:
		print('[ Error ] Runtools -> main: ' + str(e))

