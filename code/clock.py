import datetime
import time
import display
import g_calendar
import logging
# import clockconnect
import tcpserver

#         red       orange    yellow    green     blue      turq.     violet
colors = [0xe74c3c, 0xe67e22, 0xf1c40f, 0x2ecc71, 0x3498db, 0x1abc9c, 0x9b59b6]

next_update_clock = 0
next_update_calendar = 0
next_calendar_notification = 0

def update_clock():
    time_now = datetime.datetime.now().time()
    hour = time_now.hour if time_now.hour <= 12 else time_now.hour - 12
    color = colors[time_now.minute / 15]
    display.set_display(hour, hour < 10, color)

def infinity():
    sequence = [1, 2, 6, 5, 4, 3, 6, 7]
    current_color = 0
    for loops in range(8):
        for i in sequence:
            display.clear()
            display.set_display_manual({i: colors[current_color % 7]})
            current_color += 1
            time.sleep(0.08)

def attention_dp():
    for i in range(24):
        display.set_display_manual({0: colors[i % 6]})
        time.sleep(2.0 / 24.0)
    display.set_display_manual({0: 0})
    time.sleep(1)

def blink_events():
    dp_off_color = display.current_color if display.decimal_on else 0
    for event in g_calendar.events:
        if "colorId" in event:
            display.set_display_manual({0: g_calendar.color_ids[event["colorId"]]})
        else:
            display.set_display_manual({0: 0xffffff})

        time.sleep(0.5)
        display.set_display_manual({0: 0})
        time.sleep(0.5)

    display.set_display_manual({0: dp_off_color})

# main
display.init()
infinity()
display.clear()
g_calendar.init()
# tcp_server = clockconnect.Server()
tcpserver.init()
logging.basicConfig(filename='CLOCK.log', level=logging.INFO)
logging.info(str(time.time())+" : started")
while True:
    try:
        if not tcpserver.connected:
            if time.time() > next_update_calendar:
                logging.info(str(time.time())+" : update calendar")
                next_update_calendar = time.time() + 5
                new = g_calendar.update()
                if new:
                    next_calendar_notification = time.clock()

            if time.time() > next_calendar_notification:
                logging.info(str(time.time())+" : notification")
                next_calendar_notification = time.time() + 30
                if len(g_calendar.events):
                    attention_dp()
                    blink_events()

            if time.time() > next_update_clock:
                logging.info(str(time.time())+" : update clock")
                next_update_clock = time.time() + 30
                update_clock()
    except Exception as e:
        logging.error(str(time.time())+' : EXCEPTION : ' + str(e))
    time.sleep(1)
