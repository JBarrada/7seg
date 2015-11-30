from neopixel import *
import time

LED_COUNT = 8
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 120

strip = None
current_color = 0xff0000
decimal_on = False

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
    return (int(r) << 16) | (int(g) << 8) | int(b)


def set_display_fade(char, dp, color, f_time):
    global strip, current_color, decimal_on, strip_colors
    current_color = color
    decimal_on = dp

    strip_steps = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

    for i in range(8):
        if (i in chars[char]) or ((i == dp_seg) and dp):
            strip_steps[i] = calculate_step(strip_colors[i], color_to_rgb(color), f_time/10)
        else:
            strip_steps[i] = calculate_step(strip_colors[i], color_to_rgb(0), f_time/10)

    for step in range(f_time/10):
        for i in range(8):
            r, g, b = strip_colors[i]
            r += strip_steps[i][0]
            g += strip_steps[i][1]
            b += strip_steps[i][2]

            set_pixel_proxy(i, (r, g, b))
        strip.show()
        time.sleep((f_time/10)/1000.0)

    set_display(char, dp, color)


def calculate_step((fr, fg, fb), (tr, tg, tb), step):
    return (tr-fr)/float(step), (tg-fg)/float(step), (tb-fb)/float(step)


def set_display(char, dp, color):
    global strip, current_color, decimal_on
    current_color = color
    decimal_on = dp
    for i in range(8):
        if (i in chars[char]) or ((i == dp_seg) and dp):
            set_pixel_proxy(i, color_to_rgb(color))
        else:
            set_pixel_proxy(i, color_to_rgb(0))
    strip.show()


def set_display_manual(seg_and_color):
    global strip
    for key in seg_and_color:
        set_pixel_proxy(key, color_to_rgb(seg_and_color[key]))
    strip.show()


def set_pixel_proxy(i, (r, g, b)):
    global strip, strip_colors
    strip.setPixelColor(i, rgb_to_color(r, g, b))
    strip_colors[i] = (r, g, b)


def clear():
    global strip
    for i in range(8):
        set_pixel_proxy(i, color_to_rgb(0))
    strip.show()


def init():
    global strip
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, False, LED_BRIGHTNESS)
    strip.begin()
