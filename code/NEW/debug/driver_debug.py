from debug_graphics import *
import threading
import time
import color_tools

a_rect, b_rect, c_rect, d_rect, e_rect, f_rect, g_rect, dprect = [None]*8
rects = None
win = None

seg_pos = [4, 5, 7, 1, 2, 3, 6, 0]


def push(segments):
    global rects, seg_pos
    for i in range(8):
        r, g, b = segments[i]
        r = (r/2.0) + 128.0
        g = (g/2.0) + 128.0
        b = (b/2.0) + 128.0
        rects[seg_pos[i]].setFill(color_rgb(r, g, b))


def init_thread():
    global win, a_rect, b_rect, c_rect, d_rect, e_rect, f_rect, g_rect, dprect, rects
    win = GraphWin('Clock Debug', 320, 440)
    win.setBackground(color_rgb(64, 64, 64))

    a_rect = Rectangle(Point(40, 0), Point(200, 40))
    b_rect = Rectangle(Point(200, 40), Point(240, 200))
    c_rect = Rectangle(Point(200, 240), Point(240, 400))
    d_rect = Rectangle(Point(40, 440), Point(200, 400))
    e_rect = Rectangle(Point(0, 400), Point(40, 240))
    f_rect = Rectangle(Point(0, 200), Point(40, 40))
    g_rect = Rectangle(Point(40, 240), Point(200, 200))
    dprect = Rectangle(Point(280, 440), Point(320, 400))

    rects = [dprect, d_rect, e_rect, f_rect, a_rect, b_rect, g_rect, c_rect]
    for r in rects:
        r.setWidth(0)
        r.setFill(color_rgb(128, 128, 128))
        r.draw(win)

    while True:
        for r in rects:
            r.setWidth(0)
        time.sleep(1.0/30.0)


def init():
    t = threading.Thread(target=init_thread)
    t.daemon = True
    t.start()
