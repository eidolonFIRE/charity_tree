from patterns.base import base, State
from random import randint, shuffle
from color_utils import to_color


class classic(base):
    def __init__(self, strip_length):
        strip_length = strip_length - (strip_length % 4)
        self.strip_order = list(range(0, strip_length, 4))
        shuffle(self.strip_order)
        super(classic, self).__init__(strip_length)

    def clear(self):
        self.dots = []

    def newDot(self, leds, idx):
        x = self.strip_order[idx] + randint(0, 3)
        leds[x] = to_color(1.0, 0.9, 0.6)
        return [x, randint(50, 1000)]

    def _step(self, state, leds):
        for i in range(len(self.dots)):
            if self.dots[i][1] == 0:
                leds[self.dots[i][0]] = to_color()
                if state != State.STOP:
                    self.dots[i] = self.newDot(leds, i)
                else:
                    del self.dots[i]
                    if len(self.dots) == 0:
                        shuffle(self.strip_order)
                        return State.OFF
            else:
                self.dots[i][1] -= 1
        if state == State.START:
            if len(self.dots) < len(self.strip_order):
                self.dots.append(self.newDot(leds, len(self.dots)))
            else:
                return State.RUNNING
        return state
