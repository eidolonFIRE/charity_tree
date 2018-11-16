from patterns.base import base, State
from random import shuffle, randint, random
from time import time
from utils import to_color, mult_color, blend_color, wheel


class seasonal(base):
    def __init__(self, numPixels):
        super(seasonal, self).__init__(numPixels)
        self.trunk_end = 10
        self.trunk_taper = 40
        self.noise_color = [0] * numPixels
        self.noise_bri = [1.0] * numPixels

    def _step(self, state, strip):
        for pos in range(self.numPx):

            # blend from base to leaves
            if randint(0, 3) == 0:
                self.noise_color[pos] = min(30, max(0, self.noise_color[pos] + randint(-1,1)))
            self.noise_bri[pos] = min(1.0, max(0.0, self.noise_bri[pos] + (random() - 0.499) / 5.0))

            base_color = to_color(240,200,120)
            leaf_color = mult_color(wheel(abs((int(time() * 2.0)) % 150 - 75) + self.noise_color[pos]), self.noise_bri[pos])

            if state == State.STOP:
                px_color = 0x0
            if pos < self.trunk_end:
                px_color = mult_color(base_color, self.noise_bri[pos])
            elif pos < self.trunk_end + self.trunk_taper:
                px_color = blend_color(leaf_color, mult_color(base_color, self.noise_bri[pos]), float(pos - self.trunk_end) / float(self.trunk_taper))
            else:
                px_color = leaf_color

            strip._led_data[pos] = px_color

        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF

        return state
