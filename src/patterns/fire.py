from patterns.base import base, State
from random import randint, random
from time import time
from color_utils import to_color, color_blend


class fire(base):
    def __init__(self, strip_length):
        super(fire, self).__init__(strip_length)

    def clear(self):
        pass

    def _step(self, state, leds):
        # scan from top to bottom
        for pos in range(self.len - 1, 0, -1):
            leds[pos] = color_blend(leds[pos], leds[pos - 1], random()**4) * 0.95

        # add fire
        for x in range(2):
            bri = random()**2
            leds[int(random()**3 * self.len)] = to_color(1.0, bri, bri / (1.0 + random()))

        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF
