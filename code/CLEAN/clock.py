import datetime
import dateutil.parser
import time
import g_calendar
import tcpserver

try:
    import display
except Exception as e:
    import DEBUG_display as display
    debug = True

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

def attention_dp():
    for i in range(24):
        display.set_display_manual({0: colors[i % 6]})
        time.sleep(2.0 / 24.0)
    display.set_display_manual({0: 0})
    time.sleep(1)

def blink_events():
    for event in g_calendar.events:
        blink_color = g_calendar.color_ids[event["colorId"]] if "colorId" in event else 0xffffff

        event_date = dateutil.parser.parse(event['start']['dateTime'] if 'dateTime' in event['start'] else event['start']['date'])

        event_date = event_date.replace(tzinfo=None)
        delta = event_date - datetime.datetime.now()

        if delta < datetime.timedelta(hours=10):
            display.clear()
            time.sleep(0.5)
            display.set_display(int(delta.seconds / 3600), True, blink_color)
            time.sleep(0.5)
            display.set_display(16, False, blink_color)
            time.sleep(0.5)
            display.clear()
        else:
            display.set_display_manual({0: blink_color})
            time.sleep(0.5)
            display.set_display_manual({0: 0})
        time.sleep(0.5)

# main
display.init()
# display.clear()
g_calendar.init()
tcpserver.init()
while True:
    try:
        if not tcpserver.connected:
            if time.time() > next_update_calendar:
                next_update_calendar = time.time() + 5
                new = g_calendar.update()
                if new:
                    next_calendar_notification = time.clock()

            if time.time() > next_calendar_notification:
                next_calendar_notification = time.time() + 30
                if len(g_calendar.events):
                    attention_dp()
                    blink_events()
                    update_clock()

            if time.time() > next_update_clock:
                next_update_clock = time.time() + 30
                update_clock()
    except Exception as e:
        pass
    time.sleep(1)
