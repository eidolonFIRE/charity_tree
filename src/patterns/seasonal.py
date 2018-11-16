from patterns.base import base, State
from random import shuffle, randint, random
from time import time
from utils import to_color, mult_color, blend_color, wheel


class seasonal(base):
    def __init__(self, numPixels):
        super(seasonal, self).__init__(numPixels)
        self.full_stop = True
        self.trunk_end = numPixels / 4
        self.trunk_taper = 30
        self.noise_color = [0] * numPixels
        self.noise_bri = [1.0] * numPixels

    def clear(self):
        self.i = 0
        self.cleared = 0
        shuffle(self.strip_order)

    def _step(self, state, strip):
        for t in range(10):
            if self.i >= len(self.strip_order):
                self.i = 0
                if state == State.START:
                    return State.RUNNING
            if self.i == 0 and state == State.STOP:
                if self.cleared == 2:
                    self.cleared = 0
                    return State.OFF
                self.cleared += 1
            pos = self.strip_order[self.i]

            # blend from base to leaves
            self.noise_color[pos] = min(30, max(0, self.noise_color[pos] + randint(-1,1)))
            self.noise_bri[pos] = min(1.0, max(0.0, self.noise_bri[pos] + (random() - 0.499) / 4.0))

            base_color = to_color(240,200,120)
            leaf_color = mult_color(wheel(abs((int(time() * 2.0)) % 150 - 75) + self.noise_color[pos]), self.noise_bri[pos])

            if state == State.STOP:
                px_color = 0x0
            if pos < self.trunk_end:
                px_color = base_color
            elif pos < self.trunk_end + self.trunk_taper:
                px_color = blend_color(leaf_color, base_color, (pos - self.trunk_end) / float(self.trunk_taper))
            else:
                px_color = leaf_color

            strip._led_data[pos] = px_color
            self.i += 1

        return state
