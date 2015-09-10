from neopixel import *

LED_COUNT = 8
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 120

strip = None
current_color = 0
decimal_on = False

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

def set_display(char, dp, color):
    global strip, current_color, decimal_on
    current_color = color
    decimal_on = dp
    for i in range(8):
        if (i in chars[char]) or ((i == dp_seg) and dp):
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, 0)
    strip.show()

def set_display_manual(seg_and_color):
    global strip
    for key in seg_and_color:
        strip.setPixelColor(key, seg_and_color[key])
    strip.show()

def clear():
    global strip
    for i in range(8):
        strip.setPixelColor(i, 0)
    strip.show()

def init():
    global strip
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, False, LED_BRIGHTNESS)
    strip.begin()