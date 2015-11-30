import datetime
import dateutil.parser
import threading
import display
import time
import color_tools
import pywapi


def show_clock():
    time_now = datetime.datetime.now().time()
    hour = time_now.hour if time_now.hour <= 12 else time_now.hour - 12
    color = display.palette[[0, 1, 4, 6][time_now.minute / 15]]
    display.display_char_fade(str(hour), color, 600)


def show_temp():
    yahoo_weather = pywapi.get_weather_from_yahoo('78728', 'imperial')
    for ch in yahoo_weather['condition']['temp']:
        display.display_char_fade(ch, color_tools.random_rgb(), 300)
    display.display_char_fade(chr(0xb0), color_tools.random_rgb(), 300)
    display.display_char_fade('f', color_tools.random_rgb(), 300)
    time.sleep(0.4)


def show_weather():
    yahoo_weather = pywapi.get_weather_from_yahoo('78728', 'imperial')
    code = int(yahoo_weather['condition']['code'])
    display.display_weather_code(code, 1)


tasks = [[show_clock, 0, 30, False], [show_temp, 0, 60, True], [show_weather, time.time() + 30, 60, True]]

display.driver.init()
time.sleep(1)
while 1:
    for task_num in range(len(tasks)):
        if time.time() > tasks[task_num][1]:
            if tasks[task_num][3]:
                display.attention_dp()
                tasks[task_num][0]()
                show_clock()
            else:
                tasks[task_num][0]()
            tasks[task_num][1] = time.time() + tasks[task_num][2]
