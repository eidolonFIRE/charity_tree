from patterns.base import base, State
from random import shuffle, randint, random
from time import time
from utils import wheel


class rainbow2(base):
    def __init__(self, numPixels):
        super(rainbow2, self).__init__(numPixels)
        self.buff = [0] * numPixels
        self.full_stop = True
        self.scale = 1.0
        self.scale_t = 1.0
        self.time = 0.0
        self.speed = 1.0
        self.speed_t = 1.0

    def clear(self):
        self.i = 0
        self.cleared = 0
        self.start_time = time()
        shuffle(self.strip_order)

    def _step(self, state, strip):
        if randint(0, 20) == 0:
            self.scale_t = random() * 5 + 0.2
        if randint(0, 20) == 0:
            self.start_time = time() + self.start_time
            self.speed_t = (random() - 0.5) * 10.0
        self.speed += (self.speed_t - self.speed) * 0.01
        self.scale += (self.scale_t - self.scale) * 0.01

        self.time += self.speed

        for t in range(20):
            if self.i >= len(self.strip_order):
                self.i = 0
                if state == State.START:
                    self.buff = strip._led_data
                    return State.RUNNING
            if self.i == 0 and state == State.STOP:
                if self.cleared == 2:
                    self.cleared = 0
                    return State.OFF
                self.cleared += 1
            pos = self.strip_order[self.i]
            color = wheel((int(pos * self.scale) + int(self.time)) % 256) if state != State.STOP else 0x0
            self.buff[pos] = color
            self.i += 1

        return state
