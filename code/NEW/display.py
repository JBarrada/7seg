import threading
import time
import color_tools
import clock_ascii
import weather_codes
try:
    import driver
except ImportError as e:
    from debug import driver_debug as driver

palette = [color_tools.color_to_rgb(0xe74c3c), color_tools.color_to_rgb(0xe67e22),
           color_tools.color_to_rgb(0xf1c40f), color_tools.color_to_rgb(0x2ecc71),
           color_tools.color_to_rgb(0x3498db), color_tools.color_to_rgb(0x1abc9c), color_tools.color_to_rgb(0x9b59b6)]

segments = [[0, 0, 0]]*8


def attention_dp():
    global segments
    for i in range(360):
        segments[7] = color_tools.h_to_rgb((i*4) % 360)
        push_segs()
        time.sleep(2.0/360.0)

    segments[7] = (0, 0, 0)
    push_segs()


def display_char(char, (r, g, b)):
    global segments
    segments = [[0, 0, 0]]*8
    for i in clock_ascii.char_segs(char):
        segments[i] = (r, g, b)
    push_segs()


def display_char_fade(char, (r, g, b), duration):
    global segments
    frame = [[0, 0, 0]]*8
    for i in clock_ascii.char_segs(char):
        frame[i] = (r, g, b)

    fade_frame(frame, duration)


def display_weather_code(code, loops):
    global segments
    animation = weather_codes.codes[code]
    for loop in range(loops):
        for frame in animation:
            if frame[0]:
                fade_frame(frame[2], frame[1])
            else:
                segments = frame[2]
                push_segs()
                time.sleep(frame[1]/1000.0)


def fade_frame(frame, duration):
    segment_steps = [[0, 0, 0]]*8
    for i in range(8):
        segment_steps[i] = calculate_step(segments[i], frame[i], duration/10.0)

    for step in range(duration/10):
        for i in range(8):
            r, g, b = segments[i]
            segments[i] = [r+segment_steps[i][0], g+segment_steps[i][1], b+segment_steps[i][2]]
        push_segs()
        time.sleep((duration/10.0)/1000.0)


def calculate_step((fr, fg, fb), (tr, tg, tb), step):
    return (tr-fr)/float(step), (tg-fg)/float(step), (tb-fb)/float(step)


def push_segs():
    global segments
    driver.push(segments)
