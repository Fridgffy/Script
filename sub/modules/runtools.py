#! /usr/bin/env python

import os
import sys
import time
import subprocess


# 执行命令 之前判断是否有这个进程在运行
def start(shell_file, interval, r_path, o_path):
	try:
		print(f'interval: {interval}')
		p = subprocess.Popen(shell_file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p.wait()
		if p.returncode == 0:
			print(f'success')
		else:
			print()
	except Exception as e:
		print('[ Error ] Runtools -> start: ' + str(e))
		sys.exit(1)











# main
def main(interval, r_path, o_path, shell_path):
	try:
		for shell_file in os.listdir(shell_path):
			start(shell_file, interval, r_path, o_path)
		# start function 
		# start(interval)
	except Exception as e:
		print('[ Error ] Runtools -> main: ' + str(e))
