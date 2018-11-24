from patterns.base import base, State
from random import random, randint, shuffle
from color_utils import color_wheel


class watercolor(base):
    def __init__(self, strip_length):
        self.strip_order = list(range(strip_length))
        shuffle(self.strip_order)
        super(watercolor, self).__init__(strip_length)

    def clear(self):
        self.i = 0
        self.cleared = 0
        self.baseC = random()
        self.dots = []

    def newDot(self):
        return [randint(0, self.len - 1), color_wheel(self.baseC + random() / 10.0, random() / 2.0 + 0.5)]

    def _step(self, state, leds):
        if state == State.START:
            return State.RUNNING
        # convolution filter on led strip
        for t in range(30):
            if self.i >= len(self.strip_order):
                self.i = 0
                shuffle(self.strip_order)
            if self.i == 0 and state == State.STOP:
                if self.cleared == 2:
                    self.cleared = 0
                    return State.OFF
                self.cleared += 1
            pos = self.strip_order[self.i]
            leds[pos] = (leds[pos - 1] + leds[pos] + leds[(pos + 1) % self.len]) / 3.0
            self.i += 1
        if state != State.STOP:
            # update base dots
            for t in self.dots:
                leds[t[0]] = t[1]
            # add dots
            if len(self.dots) < 6 and self.loopCount % 10 == 0:
                self.dots.append(self.newDot())
            # base color
            if randint(0, 50) == 0 and len(self.dots) > 1:
                i = randint(0, len(self.dots) - 1)
                self.dots[i] = self.newDot()
            # color burst
            if randint(0, 100) == 0:
                i = randint(0, self.len - 5)
                c = color_wheel(random())
                for x in range(4):
                    leds[i + x] = c
            # change base color
            if randint(0, 200) == 0:
                self.baseC = random()
