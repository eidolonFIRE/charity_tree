from enum import Enum


class State(Enum):
    UNKNOWN = -1
    OFF = 0
    START = 1
    RUNNING = 2
    STOP = 3
    HARDSTOP = 4


class base(object):
    def __init__(self, strip_length):
        self.len = strip_length
        self.state = State.START
        self.one_shot = False
        self.loopCount = 0
        self.clear()

    def clear(self):
        pass

    def step(self, leds):
        self.loopCount += 1
        self.state = self._step(self.state, leds) or self.state
