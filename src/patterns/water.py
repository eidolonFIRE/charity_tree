from patterns.base import base, State
from random import random, uniform
from time import time
from color_utils import to_color, color_blend
import math


class Wave():
    def __init__(self, strip_length):
        self.reset()
        self.freq = self.freq_t
        self.offset = self.offset_t
        self.scale = self.scale_t
        self.reset()
        self.elapsed = 0.0
        self.mid = strip_length / 2

    def reset(self):
        self.duration = uniform(5.0, 20.0)
        self.freq_t = (random() - 0.5) * 4.0
        self.offset_t = random() * 20.0
        self.scale_t = (random() + 0.02) / 3.0

    def step(self, delta_time):
        self.duration -= delta_time
        self.elapsed += delta_time * self.freq
        if self.duration < 0:
            self.reset()
        self.freq += (self.freq_t - self.freq) * 0.01
        self.offset += (self.offset_t - self.offset) * 0.01
        self.scale += (self.scale_t - self.scale) * 0.01

    def get(self, pos):
        return (math.sin((pos - self.mid) * self.scale + self.offset + self.elapsed) + 1) / 2.0


class water(base):
    def __init__(self, strip_length):
        super(water, self).__init__(strip_length)
        self.waves = [Wave(strip_length) for x in range(4)]
        self.waves_g = [Wave(strip_length) for x in range(2)]

    def clear(self):
        self.prev_time = time()
        self.fade_in = 0

    def _step(self, state, leds):
        delta_time = time() - self.prev_time

        # step for each Wave
        for each in self.waves:
            each.step(delta_time)
        for each in self.waves_g:
            each.step(delta_time)

        # concat waves
        for pos in range(0, self.len):
            b = self.waves[0].get(pos) * self.waves[1].get(pos) + self.waves[2].get(pos) * self.waves[3].get(pos)
            g = self.waves_g[0].get(pos) * self.waves_g[1].get(pos)
            if state == State.START:
                leds[pos] = color_blend(to_color(0.0, b * g, b), leds[pos], (self.fade_in / 5.0) ** 2)
            else:
                leds[pos] = to_color(0.0, b * g, b)

        # simple state machine
        if state == State.START:
            self.fade_in += delta_time
            if self.fade_in > 5:
                return State.RUNNING
        elif state == State.STOP:
            return State.OFF

        self.prev_time = time()
