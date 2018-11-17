from patterns.base import base, State
from random import shuffle, randint, random
from time import time
from utils import to_color, mult_color, blend_color, wheel


class seasonal(base):
    def __init__(self, numPixels):
        super(seasonal, self).__init__(numPixels)
        self.trunk_taper = 50
        self.noise_color = [0] * numPixels
        self.noise_bri = [1.0] * numPixels
        self.noise_bri_t = [1.0] * numPixels
        self.max_noise_color = 10

    def _step(self, state, strip):
        for pos in range(self.numPx):
            if randint(0, 15) == 0:
                self.noise_color[pos] = min(self.max_noise_color, max(0, self.noise_color[pos] + randint(-1,1)))
            # sporatically assign a target brightness for the led
            if randint(0, 20) == 0:
                self.noise_bri_t[pos] = random()**2
            # adjust brightness toward target
            self.noise_bri[pos] = self.noise_bri[pos] + (self.noise_bri_t[pos] - self.noise_bri[pos]) * 0.05

            base_color = mult_color(to_color(220, 200, 80), self.noise_bri[pos])
            leaf_color = wheel(abs((time() * 1.0) % 150 - 75) + self.noise_color[pos], self.noise_bri[pos])

            if state != State.RUNNING:
                px_color = 0x0
            elif pos < self.trunk_taper:
                # blend from base to leaves
                px_color = blend_color(leaf_color, base_color, float(pos) / float(self.trunk_taper))
            else:
                px_color = leaf_color

            strip._led_data[pos] = px_color

        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF

        return state
