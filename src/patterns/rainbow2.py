from patterns.base import base, State
from random import shuffle, randint, random
from time import time
from utils import wheel, to_color


class rainbow2(base):
    def __init__(self, numPixels):
        super(rainbow2, self).__init__(numPixels)
        self.scale = 1.0
        self.scale_t = 1.0
        self.time = 0.0
        self.speed = 1.0
        self.speed_t = 1.0

    def _step(self, state, strip):
        # update sweeping
        if randint(0, 20) == 0:
            self.scale_t = random() * 10.0 + 0.2
        if randint(0, 20) == 0:
            self.speed_t = (random() - 0.5) * 20.0
        self.speed += (self.speed_t - self.speed) * 0.01
        self.scale += (self.scale_t - self.scale) * 0.002
        self.time += self.speed

        # update LEDs
        for pos in range(self.numPx):
            color = wheel(pos * self.scale + self.time) if state != State.STOP else 0x0
            strip._led_data[pos] = color if state == State.RUNNING else 0

        # update state machine
        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF

        return state
