import colorsys
import random

last_hue = 0


def random_rgb():
    global last_hue
    current_hue = random.randint(0, 360)
    while 60 > abs(current_hue-last_hue) > 300:
        current_hue = random.randint(0, 360)
    last_hue = current_hue
    r, g, b = colorsys.hsv_to_rgb(last_hue/360.0, 1, 1)
    return r*255.0, g*255.0, b*255.0


def h_to_rgb(hue):
    r, g, b = colorsys.hsv_to_rgb(hue/360.0, 1, 1)
    return r*255.0, g*255.0, b*255.0


def color_to_rgb(color):
    return float(color >> 16 & 0xff), float(color >> 8 & 0xff), float(color & 0xff)


def rgb_to_color(r, g, b):
    return (int(r) << 16) | (int(g) << 8) | int(b)
