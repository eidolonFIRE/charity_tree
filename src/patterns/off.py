from patterns.base import PatternBase, State
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
            if state == State.START:
                return State.RUNNING
            elif state == State.STOP:
                return State.OFF
        strip.setPixelColor(self.strip_order[self.i], 0)
        self.i += 1

        return state
