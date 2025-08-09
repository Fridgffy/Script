import tkinter as tk
from PIL import ImageGrab
import time
import numpy as np
from plyer import notification
from playsound import playsound
import pyautogui
import sys
import datetime
# pip install playsound==1.2.2
# pip install Pillow


def get_coordinate():
	xy_array = []

	input("[ Hint ] 把鼠标移动到监控区域的左上角")
	position = pyautogui.position()
	x = position.x
	y = position.y
	xy_array.append(x)
	xy_array.append(y)

	input("[ Hint ] 把鼠标移动到监控区域的右下角")
	position = pyautogui.position()
	x = position.x
	y = position.y
	xy_array.append(x)
	xy_array.append(y)
	xy = tuple(xy_array)

	return xy

def get_average_color(x, y, x2, y2):
	bbox = (x, y, x2, y2)
	screenshot = ImageGrab.grab(bbox)
	screenshot_np = np.array(screenshot)
	average_color_np = screenshot_np.mean(axis=(0, 1))
	average_color = tuple(map(int, average_color_np))
	return average_color

# 告警函数
def alarm():
	notification.notify(
	title = '波分颜色变化',
	message = '波分颜色变化',
	app_name = '波分颜色变化',
	timeout = 5
	)

# 监控函数
def Monitor(COORDINATE):
	count = 1
	array_time = []

	# 获取波分区域颜色的平均值
	initial_color = get_average_color(*COORDINATE)

	print("\nStart Monitor 波分...\n")

	try:
		while True:
			current_color = get_average_color(*COORDINATE)
			now = datetime.datetime.now()

			# 如果颜色发生变化
			if current_color != initial_color:
				# 播放声音，把文件放到C盘根目录
				for i in range(0,2):
					playsound(r'C:\\12.mp3')

				# 系统告警，10分钟内只执行5次
				if count % 6 == 0:
					if time.time() - array_time[0] > 600: # 判断离第一次告警是否超过 600/10分钟
						array_time = []
						count = 1
						sys.stdout.write('\n')

						alarm()
						print('[ ' + now.strftime('%Y-%m-%d %H:%M:%S') + ' ]' + f"  波分区域颜色已变化！")
						array_time.append(time.time())
						count += 1
					else:
						sys.stdout.write(f'[ Notice ] 10 分钟内不再显示告警信息' + '，最后一次告警时间: ' + now.strftime('%Y-%m-%d %H:%M:%S') + '\r')
				else:
					alarm()
					print('[ ' + now.strftime('%Y-%m-%d %H:%M:%S') + ' ]' + f"  波分区域颜色已变化！")
					array_time.append(time.time())
					count += 1
				# 更新颜色
				# initial_color = current_color 
			# 每隔多长时间检查一次
			time.sleep(10) 
			
	except KeyboardInterrupt:
		print("\n谁把我程序给停了!")
	except Exception as e:
		print(str(e))

if __name__ == '__main__':
	logo = r"""
 _____ _          ______ _ _            __           
/  ___| |         | ___ (_) |          / _|          
\ `--.| |__   __ _| |_/ /_| |__   ___ | |_ ___ _ __  
 `--. \ '_ \ / _` | ___ \ | '_ \ / _ \|  _/ _ \ '_ \ 
/\__/ / | | | (_| | |_/ / | |_) | (_) | ||  __/ | | |
\____/|_| |_|\__,_\____/|_|_.__/ \___/|_| \___|_| |_| 每10秒检查一次时间变化
																														  
"""
	print(logo)
	print("[Notice] 别忘了把12.mp3放到C盘根目录")
	sys.stdout.write('\n')
	COORDINATE = get_coordinate()
	Monitor(COORDINATE)