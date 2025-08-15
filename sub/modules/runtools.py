import os
import sys






def judge_result_dir(result):
	try:
		# if result dir not empty
		if not os.listdir(result):
			return True
		else:
			return False
	except Exception as e:
		print('[ Error ] runtools.py -> judge_result_dir: ' + str(e))
		sys.exit(1)



# 执行命令 之前判断是否有这个进程在运行

# main
def main(result):
	try:
		if judge_result_dir(result):
			print('kong')
		else:
			print('[ Error ] result dir is not empty!')
			sys.exit(1)
	except Exception as e:
		print('[ Error ] runtools.py -> main: ' + str(e))



