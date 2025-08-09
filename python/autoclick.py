# coding: utf-8
import pyautogui
import time
import sys
import datetime

TIME_INTERVAL = 60
COUNT = 1

def GetPosition():
	input("[ Hint ] 把鼠标放在告警的那个红点上别动")
	position = pyautogui.position()
	x = position.x
	y = position.y
	position = (x,y)
	return position

def main():
	global COUNT
	now = datetime.datetime.now()
	# sys.stdout.write(f"自动点击ITSM平台告警，时间间隔为{TIME_INTERVAL/60}分钟\n")
	sys.stdout.write(f"[ Notice ] 启动时间为：" + now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
	try:
		position = GetPosition()
		x = position[0]
		y = position[1]
		sys.stdout.write(f"\n[ Notice ] 鼠标坐标为{x},{y}\n\n")

		while True:
			sys.stdout.write(f"\r[ RUNNING ] 运行了{COUNT}次 ")
			pyautogui.click(x=x, y=y)
			time.sleep(TIME_INTERVAL)
			
			COUNT =  COUNT + 1
	except Exception as e:
		print(str(e))
	except KeyboardInterrupt:
		sys.stdout.write("\n\n谁把我程序给中断了！\n")

if __name__ == '__main__':
	logo = r'''
 _____ _          ______ _   _____ _____ ________  ___
/  ___| |         | ___ (_) |_   _|_   _/  ___|  \/  |
\ `--.| |__   __ _| |_/ /_    | |   | | \ `--.| .  . |
 `--. \ '_ \ / _` | ___ \ |   | |   | |  `--. \ |\/| |
/\__/ / | | | (_| | |_/ / |  _| |_  | | /\__/ / |  | |
\____/|_| |_|\__,_\____/|_|  \___/  \_/ \____/\_|  |_/自动点击ITSM平台告警，时间间隔为5分钟
                                                      
'''
	print(logo)
	main()
