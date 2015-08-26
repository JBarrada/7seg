import colorsys
import random
import socket
import time
import threading

class Effects:
    def __init__(self, conn):
        self.conn = conn  # tcp connection

        self.segments = [(0.0, 0.0, 0.0)]*8  # hsv representation

        self.current_color = (0.0, 0.0, 0.0)
        self.color_speed = 0.001
        self.color_decay = 0.02

        self.spin_direction = 1  # clockwise
        self.spin_position = 0
        self.spin_buffer = 0.0
        self.spin_speed = 0.05

        self.l = threading.Thread(target=self.loop)
        self.l.daemon = True
        self.l.start()

    def spin(self, color):
        a = [1, 2, 3]
        b = [4, 5, 7]

        self.spin_position += self.spin_direction
        self.spin_position = (3 + self.spin_position) if self.spin_position < 0 else self.spin_position
        self.spin_position = (self.spin_position - 3) if self.spin_position > 2 else self.spin_position

        min_v = 0.6

        self.segments[a[self.spin_position]] = (color[0], 1.0, max(min_v, self.segments[a[self.spin_position]][2]))
        self.segments[b[self.spin_position]] = (color[0], 1.0, max(min_v, self.segments[b[self.spin_position]][2]))

    def beat(self):
        min_dist = 0.2
        next_h = random.uniform(0.0, 1.0 - min_dist) + self.current_color[0]
        next_h = next_h - 1.0 if next_h > 1.0 else next_h
        self.current_color = (next_h, 1.0, 1.0)

        for i in range(8):
            self.segments[i] = self.current_color

    def decay(self):
        for i in range(8):
            self.segments[i] = (self.segments[i][0], self.segments[i][1], max(0, self.segments[i][2] - self.color_decay))

    def send_to_display(self):
        data = []
        for i in range(8):
            rgb = colorsys.hsv_to_rgb(self.segments[i][0], self.segments[i][1], self.segments[i][2])
            data.append(min(int(rgb[0]*255), 255))
            data.append(min(int(rgb[1]*255), 255))
            data.append(min(int(rgb[2]*255), 255))
        # send through tcp
        self.conn.sendall(str(bytearray(data)))

    def advance(self):
        self.decay()

        next_h = self.current_color[0] + self.color_speed
        next_h = next_h - 1.0 if next_h > 1.0 else next_h
        self.current_color = (next_h, 1.0, 1.0)

        self.spin_buffer += self.spin_speed
        if self.spin_buffer > 1.0:
            self.spin_buffer = 0.0
            self.spin(self.current_color)

        self.send_to_display()

    def loop(self):
        while True:
            self.advance()
            time.sleep(1.0 / 30.0)  # 30 times a second
