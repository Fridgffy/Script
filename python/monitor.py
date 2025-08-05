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
    count = 0
    xy_array = []
    while True:
        if count == 0:
            print('[Hint] 用5秒钟时间把鼠标移动到开始位置')
            time.sleep(5)

            # 获取鼠标当前位置的坐标
            x, y = pyautogui.position()
            # print(f'当前鼠标位置的坐标是：x={x}, y={y}')
            xy_array.append(x)
            xy_array.append(y)
            count += 1
        elif count == 1:
            print('[Hint] 再用5秒钟时间把鼠标移动到结束位置')
            time.sleep(5)

            # 获取鼠标当前位置的坐标
            x, y = pyautogui.position()
            # print(f'当前鼠标位置的坐标是：x={x}, y={y}')
            xy_array.append(x)
            xy_array.append(y)
            count += 1
        else:
            break

    xy = tuple(xy_array)
    return xy


def get_average_color(x, y, x2, y2):
    bbox = (x, y, x2, y2)
    screenshot = ImageGrab.grab(bbox)
    screenshot_np = np.array(screenshot)
    average_color_np = screenshot_np.mean(axis=(0, 1))
    average_color = tuple(map(int, average_color_np))
    return average_color

# 监控函数
def Monitor(COORDINATE):
    # 获取波分区域颜色的平均值
    initial_color = get_average_color(*COORDINATE)
    # sys.stdout.write(f'Initial color coordinate is : {initial_color}\n')

    print("\nStart Monitor 波分...\n")
    try:
        while True:
            current_color = get_average_color(*COORDINATE)
            now = datetime.datetime.now()
            # 如果颜色发生变化
            if current_color != initial_color:
                print('[ ' + now.strftime('%Y-%m-%d %H:%M:%S') + ' ]' + f"  波分区域颜色已变化！")
                # 播放声音，把文件放到C盘根目录
                playsound(r'C:\\1.mp3')
                # 系统告警
                notification.notify(
                    title = '波分颜色变化',
                    message = '波分颜色变化',
                    app_name = '波分颜色变化',
                    timeout = 5
                    )
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
    print("[Notice] 别忘了把1.mp3放到C盘根目录")

    COORDINATE = get_coordinate()
    Monitor(COORDINATE)