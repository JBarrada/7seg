import datetime
import time

def g_time():
    time_now = datetime.datetime.now().time()
    hour = time_now.hour if time_now.hour <= 12 else time_now.hour - 12

    color = ['RED', 'ORANGE', 'YELLOW', 'GREEN'][time_now.minute / 15]
    print('%01x %s' % (hour, color))

while True:
    g_time()
    time.sleep(30)
