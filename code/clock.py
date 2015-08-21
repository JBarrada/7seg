from neopixel import *
import datetime
import time
import display

def g_time():
    time_now = datetime.datetime.now().time()
    hour = time_now.hour if time_now.hour <= 12 else time_now.hour - 12

    color = [0xd10000, 0xff6622, 0xffda21, 0x33dd00][time_now.minute / 15]
    print(hour)
    display.set_display(hour, False, color)

while True:
    g_time()
    time.sleep(30)
