#! /usr/bin/env python

import os
import sys
import time


# determine result dir is empty
def judge_result_dir(result):
	try:
		# if result dir not empty
		if not os.listdir(result):
			return True
		else:
			print('[ Error ] result dir is not empty!')
			sys.exit(1)
	except Exception as e:
		print('[ Error ] Runtools -> judge_result_dir: ' + str(e))
		sys.exit(1)



# 执行命令 之前判断是否有这个进程在运行
def start(interval):
	shellpathname_list = [r'D:\repositories\Script\sub\shell\1.bat', r'D:\repositories\Script\sub\shell\2.bat']
	print(f'perform {len(shellpathname_list)} tools, interval {interval} second')

	for  shellpathname in shellpathname_list:
		os.system(shellpathname)
		time.sleep(interval)











# main
def main(interval,r_path,o_path):
	try:
		judge_result_dir(r_path)

		# start function 
		interval = 3
		start(interval)
	except Exception as e:
		print('[ Error ] Runtools -> main: ' + str(e))
