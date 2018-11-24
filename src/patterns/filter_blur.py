from patterns.base import base, State
from random import shuffle


class filter_blur(base):
    def __init__(self, strip_length):
        self.strip_order = list(range(strip_length))
        self.radius = 1
        super(filter_blur, self).__init__(strip_length)
        self.one_shot = True

    def clear(self):
        self.i = 0
        shuffle(self.strip_order)

    def _step(self, state, leds):
        for idx in self.strip_order:
            denominator = (self.radius * 2 + 1) - min(0, idx - self.radius) - min(0, self.len - idx)
            leds[idx] = sum(leds[max(0, idx - self.radius):min(self.len, idx + self.radius + 1)]) / denominator

        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF
