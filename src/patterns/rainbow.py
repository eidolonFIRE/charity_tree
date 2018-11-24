from patterns.base import base, State
from random import shuffle
from time import time
from color_utils import color_wheel


class rainbow(base):
    def __init__(self, strip_length):
        self.strip_order = list(range(strip_length))
        super(rainbow, self).__init__(strip_length)

    def clear(self):
        self.i = 0
        shuffle(self.strip_order)

    def _step(self, state, leds):
        for t in range(10):
            if self.i >= self.len:
                self.i = 0
                if state == State.START:
                    return State.RUNNING
            pos = self.strip_order[self.i]
            leds[pos] = color_wheel(float(pos) / 255.0 + time() / 60.0)
            self.i += 1

        if state == State.STOP:
            return State.OFF
