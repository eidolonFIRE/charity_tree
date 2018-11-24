from patterns.base import base, State
from random import shuffle
from color_utils import to_color


class off(base):
    def __init__(self, strip_length):
        self.strip_order = list(range(strip_length))
        super(off, self).__init__(strip_length)

    def clear(self):
        shuffle(self.strip_order)
        self.i = 0

    def _step(self, state, leds):
        if self.i >= self.len:
            self.i = 0
            shuffle(self.strip_order)
        leds[self.strip_order[self.i]] = to_color()
        self.i += 1

        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF
