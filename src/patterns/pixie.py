from patterns.base import base, State
from random import randint, random
from time import time
from color_utils import to_color, color_wheel, color_blend


class Light():
    def __init__(self, strip_length):
        self.len = strip_length
        self.color = random()
        self.pos = 0.0
        self.pos_t = random() * strip_length

    def new_target(self):
        self.color += random() / 20.0
        self.pos_t = max(0.0, min(self.len - 1, self.pos + (random() - 0.5) * 40))

    def step(self):
        self.pos += (self.pos_t - self.pos) * 0.1
        if abs(self.pos_t - self.pos) < 3:
            self.new_target()


class pixie(base):
    def __init__(self, strip_length):
        super(pixie, self).__init__(strip_length)

    def clear(self):
        self.lights = [Light(self.len) for x in range(8)]

    def _step(self, state, leds):
        # fade all pixels
        for pos in range(self.len):
            leds[pos] *= 0.95

        for each in self.lights:
            leds[int(each.pos)] = color_wheel(each.color)
            each.step()
        

        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF
