from patterns.base import base, State
from random import shuffle
from time import time
from color_utils import to_color, color_blend


class candycane(base):
    def __init__(self, strip_length):
        super(candycane, self).__init__(strip_length)
        self.color_a = to_color(1.0, 1.0, 1.0)
        self.color_b = to_color(1.0, 0.0, 0.0)
        self.stripe_width = 18
        self.fade_width = 5.0

    def clear(self):
        self.sweep_in = 0.0
        self.prev_time = time()

    def _step(self, state, leds):
        for pos in range(self.len):
            offset = pos - time() * 3
            if offset % (self.stripe_width * 2) > self.stripe_width:
                a = self.color_b    
                b = self.color_a     
            else:
                a = self.color_a
                b = self.color_b

            # ratio of how far through a stripe
            ratio = offset % self.stripe_width
            if ratio < self.sweep_in + self.fade_width:
                # blend in pattern
                leds[pos] = color_blend(a, leds[pos], 0.1)
            elif ratio < self.sweep_in:
                # normal pattern
                if ratio < self.fade_width:
                    leds[pos] = color_blend(a, b, ratio / self.fade_width)
                else:
                    leds[pos] = a

        # update state machine
        if state == State.START:
            self.sweep_in += (time() - self.prev_time)
            if self.sweep_in > self.stripe_width:
                self.sweep_in = self.stripe_width
                return State.RUNNING
        elif state == State.STOP:
            return State.OFF
        self.prev_time = time()
