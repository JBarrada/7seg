from DEBUG_graphics import *
import threading
import time

win = None
current_color = 0
decimal_on = False

a_seg_rect, b_seg_rect, c_seg_rect, d_seg_rect, e_seg_rect, f_seg_rect, g_seg_rect, dp_seg_rect = [None]*8
rects = None

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

    [c_seg, e_seg, f_seg, g_seg]  # h
]

def color_to_rgb(colorhex):
    return colorhex >> 16 & 0xff, colorhex >> 8 & 0xff, colorhex & 0xff

def set_display(char, dp, color):
    global rects, current_color, decimal_on
    current_color = color
    decimal_on = dp
    for i in range(8):
        if (i in chars[char]) or ((i == dp_seg) and dp):
            r, g, b = color_to_rgb(color)
            rects[i].setFill(color_rgb(r, g, b))
        else:
            rects[i].setFill(color_rgb(240, 240, 240))

def set_display_manual(seg_and_color):
    global rects
    for key in seg_and_color:
        r, g, b = color_to_rgb(seg_and_color[key])
        rects[key].setFill(color_rgb(r, g, b))

def clear():
    global rects
    for r in rects:
        r.setFill(color_rgb(240, 240, 240))

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

