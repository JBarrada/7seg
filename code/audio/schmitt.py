
class Schmitt:
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.below = False

    def feed(self, sample):
        # check if triggered
        if (sample > self.high) and self.below:
            self.below = False
            return True
        if sample < self.low:
            self.below = True
        return False
