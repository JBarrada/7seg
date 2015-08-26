import pyaudio
import math


class Doctor:
    def __init__(self, sample_rate, freq, release_time):
        self.time_constant = 1.0 / (2.0 * math.pi * freq)
        self.filter_coeff = 1.0 / (sample_rate * self.time_constant)
        self.release_coeff = math.exp(-1.0 / (sample_rate * release_time))

        self.filter1_out = 0
        self.filter2_out = 0
        self.peak_envelope = 0
        self.beat_previous = False
        self.schmitt_min = 0.3
        self.schmitt_max = 0.5

        self.min_hit = False

    def feed_sample(self, sample):
        self.filter1_out += (self.filter_coeff * (sample - self.filter1_out))
        self.filter2_out += (self.filter_coeff * (self.filter1_out - self.filter2_out))

        envelope = math.fabs(self.filter2_out)
        if envelope > self.peak_envelope:
            self.peak_envelope = envelope
        else:
            self.peak_envelope *= self.release_coeff
            self.peak_envelope += (1 - self.release_coeff) * envelope

        # beat = self.beat_previous
        # if not self.beat_previous & (self.peak_envelope > self.schmitt_max):
        #     beat = True
        # elif self.beat_previous & (self.peak_envelope < self.schmitt_min):
        #     beat = False
        #
        # event = True if beat and not self.beat_previous else False
        # self.beat_previous = beat

        if not self.min_hit & (self.peak_envelope < self.schmitt_min):
            self.min_hit = True

        max_hit = True if self.peak_envelope > self.schmitt_max else False

        event = False
        if max_hit and self.min_hit:
            self.min_hit = False
            event = True

        return event, self.peak_envelope
