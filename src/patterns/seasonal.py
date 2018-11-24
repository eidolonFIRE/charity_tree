from patterns.base import base, State
from random import randint, random
from time import time
from color_utils import to_color, color_blend, color_wheel


class seasonal(base):
    def __init__(self, strip_length):
        super(seasonal, self).__init__(strip_length)
        self.trunk_taper = 50
        self.noise_color = [1.0] * strip_length
        self.noise_color_t = [0.0] * strip_length
        self.noise_bri = [0.0] * strip_length
        self.noise_bri_t = [0.5] * strip_length

    def clear(self):
        self.sweep_in = 0

    def _step(self, state, leds):
        for pos in range(self.len):
            # sweep when starting pattern
            if pos > self.sweep_in:
                continue

            # randomly target new colors
            if randint(0, 15) == 0:
                self.noise_color_t[pos] = random() / 10.0
            if randint(0, 20) == 0:
                self.noise_bri_t[pos] = random() ** 2
            # adjust brightness toward target
            self.noise_color[pos] = (self.noise_color_t[pos] - self.noise_color[pos]) * 0.05
            self.noise_bri[pos] += (self.noise_bri_t[pos] - self.noise_bri[pos]) * 0.05

            # set the colors
            base_color = to_color(1.0, 0.8, 0.5) * self.noise_bri[pos]
            leaf_color = color_wheel(abs((time() / 150.0) % 0.6 - 0.3) + self.noise_color[pos], self.noise_bri[pos])

            if pos < self.trunk_taper:
                # blend from base to leaves
                px_color = color_blend(leaf_color, base_color, float(pos) / float(self.trunk_taper))
            else:
                px_color = leaf_color

            leds[pos] = px_color

        if state == State.START:
            self.sweep_in += 1
            if self.sweep_in > self.len:
                return State.RUNNING
        elif state == State.STOP:
            return State.OFF
