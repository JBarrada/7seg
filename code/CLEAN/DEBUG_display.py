from DEBUG_graphics import *
import threading
import time

win = None
current_color = 0xff0000
decimal_on = False

a_seg_rect, b_seg_rect, c_seg_rect, d_seg_rect, e_seg_rect, f_seg_rect, g_seg_rect, dp_seg_rect = [None]*8
rects = None

strip_colors = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

a_seg, b_seg, c_seg, d_seg, e_seg, f_seg, g_seg, dp_seg = [4, 5, 7, 1, 2, 3, 6, 0]

chars = [
    [a_seg, b_seg, c_seg, d_seg, e_seg, f_seg],  # 0
    [b_seg, c_seg],  # 1
    [a_seg, b_seg, d_seg, e_seg, g_seg],  # 2
    [a_seg, b_seg, c_seg, d_seg, g_seg],  # 3
    [b_seg, c_seg, f_seg, g_seg],  # 4
    [a_seg, c_seg, d_seg, f_seg, g_seg],  # 5
    [a_seg, c_seg, d_seg, e_seg, f_seg, g_seg],  # 6
    [a_seg, b_seg, c_seg],  # 7
    [a_seg, b_seg, c_seg, d_seg, e_seg, f_seg, g_seg],  # 8
    [a_seg, b_seg, c_seg, f_seg, g_seg],  # 9

    [a_seg, b_seg, c_seg, e_seg, f_seg, g_seg],  # A
    [a_seg, b_seg, c_seg, d_seg, e_seg, f_seg, g_seg],  # B
    [a_seg, d_seg, e_seg, f_seg],  # C
    [a_seg, b_seg, c_seg, d_seg, e_seg, f_seg],  # D
    [a_seg, d_seg, e_seg, f_seg, g_seg],  # E
    [a_seg, e_seg, f_seg, g_seg],  # F

    [c_seg, e_seg, f_seg, g_seg],  # h
    [f_seg, a_seg, b_seg, g_seg]  # degree
]


def color_to_rgb(colorhex):
    return float(colorhex >> 16 & 0xff), float(colorhex >> 8 & 0xff), float(colorhex & 0xff)


def rgb_to_color(r, g, b):
    return (r << 16) | (g << 8) | b


def set_display_fade(char, dp, color, f_time):
    global strip, current_color, decimal_on
    current_color = color
    decimal_on = dp

    strip_steps = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    #  strip_steps = []

    for i in range(8):
        if (i in chars[char]) or ((i == dp_seg) and dp):
            strip_steps[i] = calculate_step(strip_colors[i], color_to_rgb(color), f_time/10)
        else:
            strip_steps[i] = calculate_step(strip_colors[i], color_to_rgb(0xf0f0f0), f_time/10)

    for step in range(f_time/10):
        for i in range(8):
            r, g, b = strip_colors[i]
            r += strip_steps[i][0]
            g += strip_steps[i][1]
            b += strip_steps[i][2]

            set_pixel_proxy(i, (r, g, b))

        time.sleep((f_time/10)/1000.0)

    set_display(char, dp, color)


def calculate_step((fr, fg, fb), (tr, tg, tb), step):
    return (tr-fr)/float(step), (tg-fg)/float(step), (tb-fb)/float(step)


def set_display(char, dp, color):
    global rects, current_color, decimal_on
    current_color = color
    decimal_on = dp
    for i in range(8):
        if (i in chars[char]) or ((i == dp_seg) and dp):
            #  r, g, b = color_to_rgb(color)
            #  rects[i].setFill(color_rgb(r, g, b))
            set_pixel_proxy(i, color_to_rgb(color))
        else:
            set_pixel_proxy(i, color_to_rgb(0xf0f0f0))
            #  rects[i].setFill(color_rgb(240, 240, 240))


def set_display_manual(seg_and_color):
    global rects
    for key in seg_and_color:
        #  r, g, b = color_to_rgb(seg_and_color[key])
        #  rects[key].setFill(color_rgb(r, g, b))
        set_pixel_proxy(key, color_to_rgb(seg_and_color[key]))


def set_pixel_proxy(i, (r, g, b)):
    global rects
    rects[i].setFill(color_rgb(r, g, b))
    strip_colors[i] = (r, g, b)


def clear():
    global rects
    for i in range(8):
        set_pixel_proxy(i, color_to_rgb(0xf0f0f0))
        #  r.setFill(color_rgb(240, 240, 240))


def init_thread():
    global win, a_seg_rect, b_seg_rect, c_seg_rect, d_seg_rect, e_seg_rect, f_seg_rect, g_seg_rect, dp_seg_rect, rects
    win = GraphWin('!!!', 320, 440)
    win.setBackground(color_rgb(211, 211, 211))

    a_seg_rect = Rectangle(Point(40, 0), Point(200, 40))
    b_seg_rect = Rectangle(Point(200, 40), Point(240, 200))
    c_seg_rect = Rectangle(Point(200, 240), Point(240, 400))
    d_seg_rect = Rectangle(Point(40, 440), Point(200, 400))
    e_seg_rect = Rectangle(Point(0, 400), Point(40, 240))
    f_seg_rect = Rectangle(Point(0, 200), Point(40, 40))
    g_seg_rect = Rectangle(Point(40, 240), Point(200, 200))
    dp_seg_rect = Rectangle(Point(280, 440), Point(320, 400))

    rects = [dp_seg_rect, d_seg_rect, e_seg_rect, f_seg_rect, a_seg_rect, b_seg_rect, g_seg_rect, c_seg_rect]
    for r in rects:
        r.setWidth(0)
        r.setFill(color_rgb(240, 240, 240))
        r.draw(win)

    while True:
        for r in rects:
            r.setWidth(0)
        time.sleep(1.0/30.0)


def init():
    t = threading.Thread(target=init_thread)
    t.daemon = True
    t.start()

