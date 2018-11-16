from random import shuffle
from enum import Enum


class State(Enum):
    UNKNOWN = -1
    OFF = 0
    START = 1
    RUNNING = 2
    STOP = 3
    HARDSTOP = 4


class base(object):
    def __init__(self, numPixels):
        self.numPx = numPixels
        self.full_stop = False
        self.state = State.OFF
        self.loopCount = 0
        self.strip_order = list(range(numPixels))
        shuffle(self.strip_order)
        self.clear()

    def clear(self):
        pass

    def step(self, strip):
        self.loopCount += 1
        self.state = self._step(self.state, strip)
