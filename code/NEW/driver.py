from neopixel import *
from color_tools import *

strip = None

seg_pos = [4, 5, 7, 1, 2, 3, 6, 0]


def push(segments):
    global strip, seg_pos
    for i in range(8):
        r, g, b = segments[i]
        strip.setPixelColor(seg_pos[i], color_tools.rgb_to_color(r, g, b))
    strip.show()


def init():
    global strip
    strip = Adafruit_NeoPixel(8, 18, 800000, 5, False, 120)
    strip.begin()
