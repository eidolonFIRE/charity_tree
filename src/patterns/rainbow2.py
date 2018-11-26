from patterns.base import base, State
from random import randint, random
from color_utils import color_wheel, color_blend


class rainbow2(base):
    def __init__(self, numPixels):
        super(rainbow2, self).__init__(numPixels)
        self.scale = 0.01
        self.scale_t = 0.01
        self.time = 0.0
        self.speed = 0.01
        self.speed_t = 0.01

    def clear(self):
        self.sweep_in = 0

    def _step(self, state, leds):
        # update sweeping
        if randint(0, 20) == 0:
            self.scale_t = (random() - 0.5) / 5.0
        if randint(0, 20) == 0:
            self.speed_t = (random() - 0.5) / 10.0
        self.speed += (self.speed_t - self.speed) * 0.01
        self.scale += (self.scale_t - self.scale) * 0.01
        self.time += self.speed

        # update LEDs
        for pos in range(self.len):
            # fade in behavior
            if state == State.START:
                new_color = color_wheel((pos - self.len/2) * self.scale + self.time)
                if abs(sum(leds[pos] - new_color)) - random() / 10.0 < self.sweep_in:
                    leds[pos] = color_blend(leds[pos], new_color, 0.9)
            else:
                leds[pos] = color_wheel((pos - self.len/2) * self.scale + self.time)

        # update state machine
        if state == State.START:
            self.sweep_in += (3.0 - self.sweep_in) * 0.01
            if self.sweep_in >= 3.0:
                self.sweep_in = 3.0
                return State.RUNNING
        elif state == State.STOP:
            return State.OFF
