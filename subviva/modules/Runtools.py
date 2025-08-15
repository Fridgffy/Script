#! /usr/bin/env python

import os
import sys
import time
import subprocess


# 执行命令 之前判断是否有这个进程在运行
def start(shell_file, interval, r_path, o_path, p_path, shell_path):
	try:
		print(f'interval: {interval}')
		shell_pathname = os.path.join(shell_path, shell_file)
		p = subprocess.Popen(shell_pathname, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if p.stderr.read():
			print(p.stderr.read())
#		p.wait()
		print(shell_pathname)
		print(p.stdout.read())
	except Exception as e:
		print('[ Error ] Runtools -> start: ' + str(e))
		sys.exit(1)











# main
def main(interval, r_path, o_path, p_path):
	try:
		shell_path = os.path.join(p_path, 'shell')
		for shell_file in os.listdir(shell_path):
			start(shell_file, interval, r_path, o_path, p_path, shell_path)
		# start function 
		# start(interval)
	except Exception as e:
		print('[ Error ] Runtools -> main: ' + str(e))

