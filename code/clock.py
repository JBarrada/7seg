import datetime
import time
import display
import g_calendar

#         red       orange    yellow    green     blue      turq.     violet
colors = [0xe74c3c, 0xe67e22, 0xf1c40f, 0x2ecc71, 0x3498db, 0x1abc9c, 0x9b59b6]

seconds = 30

def update_clock():
    time_now = datetime.datetime.now().time()
    hour = time_now.hour if time_now.hour <= 12 else time_now.hour - 12
    color = colors[time_now.minute / 15]
    display.set_display(hour, hour < 10, color)

def infinity():
    global seconds
    sequence = [1, 2, 6, 5, 4, 3, 6, 7]
    current_color = 0
    for loops in range(8):
        for i in sequence:
            display.set_display_manual({i: colors[current_color % 7]})
            time.sleep(0.1)
        current_color += 1
    seconds += 0.1*7*8

def attention_dp():
    global seconds
    dp_off_color = display.current_color if display.decimal_on else 0
    for i in range(24):
        display.set_display_manual({0: colors[i % 6]})
        time.sleep(2.0 / 24.0)

    # return dp back to original color
    display.set_display_manual({0: dp_off_color})
    time.sleep(1)
    seconds += 3

def blink_dp(count, color):
    global seconds
    dp_off_color = display.current_color if display.decimal_on else 0
    for i in range(count):
        display.set_display_manual({0: color})
        time.sleep(0.5)
        display.set_display_manual({0: dp_off_color})
        time.sleep(0.5)
        seconds += 1

# main
display.init()
g_calendar.init()
while True:
    if seconds >= 30:
        seconds = 0
        g_calendar.update()

        if g_calendar.high_priority:
            infinity()

        update_clock()

        if g_calendar.pending_events:
            attention_dp()
            blink_dp(g_calendar.pending_events, colors[6])

    time.sleep(1)
    seconds += 1
