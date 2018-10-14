from patterns.base import PatternBase
from random import shuffle


class Off(PatternBase):
    def __init__(self, numPixels):
        super(Off, self).__init__(numPixels)

    def clear(self):
        self.i = 0

    def _step(self, state, strip):
        if self.i >= len(self.strip_order):
            self.i = 0
            shuffle(self.strip_order)
            if state == 1:
                return 2
            elif state == 3:
                return 0
        strip.setPixelColor(self.strip_order[self.i], 0)
        self.i += 1

        return state
