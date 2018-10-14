from random import shuffle


class PatternBase(object):
    def __init__(self, numPixels):
        self.numPx = numPixels
        self.state = 0
        self.loopCount = 0
        self.strip_order = list(range(numPixels))
        shuffle(self.strip_order)
        self.clear()

    def clear(self):
        pass

    def step(self, strip):
        self.loopCount += 1
        self.state = self._step(self.state, strip)
