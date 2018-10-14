from patterns.base import PatternBase
from random import shuffle
from time import time
from patterns.utils import wheel


class Rainbow(PatternBase):
    def __init__(self, numPixels):
        super(Rainbow, self).__init__(numPixels)
        self.buff = [0] * numPixels

    def clear(self):
        self.i = 0
        self.cleared = 0
        shuffle(self.strip_order)

    def _step(self, state, strip):
        for t in range(10):
            if self.i >= len(self.strip_order):
                self.i = 0
                if state == 1:
                    self.buff = strip._led_data
                    print("---rainbow full")
                    return 2
            if self.i == 0 and state == 3:
                if self.cleared == 2:
                    self.cleared = 0
                    print("---rainbow done")
                    return 0
                self.cleared += 1
            pos = self.strip_order[self.i]
            color = wheel((pos + int(time()*30)) % 256) if state != 3 else 0x0
            self.buff[pos] = color
            self.i += 1

        return state
