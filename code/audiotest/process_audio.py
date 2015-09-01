import pyaudio
import math
import schmitt


class Doctor:
    def __init__(self, sample_rate, freq, release_time):
        self.time_constant = 1.0 / (2.0 * math.pi * freq)
        self.filter_coeff = 1.0 / (sample_rate * self.time_constant)
        self.release_coeff = math.exp(-1.0 / (sample_rate * release_time))

        self.filter1_out = 0
        self.filter2_out = 0
        self.peak_envelope = 0
        # self.beat_previous = False
        self.s = schmitt.Schmitt(0.5, 0.7)

        # self.min_hit = False

    def feed_sample(self, sample):
        self.filter1_out += (self.filter_coeff * (sample - self.filter1_out))
        self.filter2_out += (self.filter_coeff * (self.filter1_out - self.filter2_out))

        envelope = math.fabs(self.filter2_out)
        if envelope > self.peak_envelope:
            self.peak_envelope = envelope
        else:
            self.peak_envelope *= self.release_coeff
            self.peak_envelope += (1 - self.release_coeff) * envelope

        event = self.s.feed(self.peak_envelope)

        return event, self.peak_envelope
