# coding: utf-8
import pyautogui
import time
import sys

TIME_INTERVAL = 5
COUNT = 1

def GetPosition():
	input("老实点，蹲下，双手抱头，把鼠标放在告警的那个红点上别动")
	position = pyautogui.position()
	x = position.x
	y = position.y
	position = (x,y)
	return position

def main():
	global COUNT
	sys.stdout.write(f"自动点击ITSM平台告警，时间间隔为{TIME_INTERVAL/60}分钟\n")
	sys.stdout.write(f"启动时间为：{time.asctime(time.localtime())}\n\n")
	try:
		position = GetPosition()
		x = position[0]
		y = position[1]
		sys.stdout.write(f"\n鼠标坐标为{x},{y}\n\n")

		while True:
			sys.stdout.write(f"\r运行了{COUNT}次 ")
			pyautogui.click(x=x, y=y)
			time.sleep(TIME_INTERVAL)
			
			COUNT =  COUNT + 1
	except Exception as e:
		sys.stdout.write(f"\n发生错误：{e}\n")
	except KeyboardInterrupt:
		sys.stdout.write("\n\n这个人！就是你，把我程序中断了！\n")

if __name__ == '__main__':
	main()
