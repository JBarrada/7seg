from neopixel import *

LED_COUNT = 8
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 255
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

"""
 AAAA
F    B
F    B
 GGGG
E    C
E    C
 DDDD  DP
"""

a_seg, b_seg, c_seg, d_seg, e_seg, f_seg, g_seg, dp_seg = range(8)  # replace with

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
]

def set_display(char, dp, color):
    for i in range(8):
        if (i in char[char]) or ((i == dp_seg) and dp):
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, 0)
    strip.show()
