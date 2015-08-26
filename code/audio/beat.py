import pyaudio
import process_audio
import socket
import effects
import struct

CHUNK = 4096

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('192.168.1.21', 46692))
e = effects.Effects(conn)

dr = process_audio.Doctor(44100, 200, 0.05)

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

    # print envelope
    # print('#'*int(envelope*20))  # pound sign VU meter
    # todo handle spin with high freq
