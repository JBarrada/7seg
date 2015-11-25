import pyaudio
import process_audio
import socket
import effects
import struct
from graphics import *

CHUNK = 2048

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('192.168.1.21', 46692))
e = effects.Effects(conn)

dr = process_audio.Doctor(44100, 400, 0.05)


win = GraphWin('!!!', 200, 200)

ln = Line(Point(0, 200), Point(100, 200))
ln.setWidth(1)

smax = Line(Point(0, 200-(dr.s.high*200)), Point(100, 200-(dr.s.high*200)))
smax.setWidth(3)
smax.setFill('blue')
smax.draw(win)

savg = Line(Point(0, 200), Point(100, 200))
savg.setWidth(3)
savg.setFill('red')
savg.draw(win)

oavg = Line(Point(0, 200), Point(100, 200))
oavg.setWidth(3)
oavg.setFill('pink')
oavg.draw(win)

brect = Rectangle(Point(100, 0), Point(200, 200))
brect.setFill('green')
brect.draw(win)
# color_rgb

colros = ['red', 'blue', 'green', 'white', 'black']
next_h = 0

# average stuff
ravgmax = 10
rollingavg = [0.0]*ravgmax
ravgpos = 0

outlier_delta = 0.1
oavgmax = 10
outlieravg = [0.0]*oavgmax
oavgpos = 0
oavgbuf_full = False


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=CHUNK, input_device_index=2)
while True:
    beat = False
    envelope = 0

    data = stream.read(CHUNK)  # todo find out if data is in the form of bytes or ints
    for i in range(0, CHUNK*2, 2):
        sample = struct.unpack('<h', data[i:i+2])[0]  # play around with '<' and '>'
        beat_temp, envelope_temp = dr.feed_sample(sample / 32768.0)
        beat = beat_temp if beat_temp else beat
        envelope += envelope_temp

    envelope /= CHUNK
    if beat:
        e.beat()
        e.spin_direction *= -1

    ln.undraw()
    ln = Line(Point(0, 200-(envelope*200)), Point(100, 200-(envelope*200)))
    ln.draw(win)
    # if beat
    if beat:
        next_h += 1
        next_h %= 5
        brect.setFill(colros[next_h])
        brect.undraw()
        brect.draw(win)

    rollingavg[ravgpos] = envelope
    ravgpos += 1
    ravgpos %= ravgmax

    avg = 0.0
    for val in rollingavg:
        avg += val
    avg /= ravgmax
    savg.undraw()
    savg = Line(Point(0, 200-(avg*200)), Point(100, 200-(avg*200)))
    savg.setWidth(3)
    savg.setFill('red')
    savg.draw(win)
    dr.s.low = avg

    if envelope-avg > outlier_delta:
        outlieravg[oavgpos] = envelope
        oavgpos += 1
        if oavgpos >= oavgmax:
            oavgpos = 0
            oavgbuf_full = True

        oa = 0.0
        if oavgbuf_full:
            for val in outlieravg:
                oa += val
            oa /= oavgmax
        else:
            for val in outlieravg[:oavgpos]:
                oa += val
            oa /= oavgpos

        oavg.undraw()
        oavg = Line(Point(0, 200-(oa*200)), Point(100, 200-(oa*200)))
        oavg.setWidth(3)
        oavg.setFill('pink')
        oavg.draw(win)
        # dr.s.high = oa + 0.09

    # print envelope
    # print('#'*int(envelope*20))  # pound sign VU meter
    # todo handle spin with high freq
