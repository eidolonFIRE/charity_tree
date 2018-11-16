from patterns.base import PatternBase, State
from random import random
from utils import *


class Twinkle(PatternBase):
    def __init__(self, numPixels):
        super(Twinkle, self).__init__(numPixels)

    def clear(self):
        self.stars = []

    def _step(self, state, strip):
        for i, x in enumerate(self.stars):
            if x[1] == 0:
                # dimming
                if x[2] == [0, 0, 0]:
                    if state == State.STOP:
                        self.stars.remove(x)
                        if len(self.stars) == 0:
                            print("---twinkle done")
                            return State.OFF
                        break
                    else:
                        while True:
                            idx = int(random() * 900) % self.numPx
                            for st in self.stars:
                                if idx == st[0]:
                                    continue
                            break
                        self.stars[i][0] = idx
                        self.stars[i][1] = 1
                else:
                    self.stars[i][2] = [max(0, int(c*9/10)) for c in x[2]]
            else:
                # brightening
                if x[2] == [255, 255, 255]:
                    self.stars[i][1] = 0
                else:
                    self.stars[i][2] = [min(255, int(c + (random()**3)*25)) for c in x[2]]
            strip.setPixelColor(x[0], to_color(*x[2]))
        if state == State.START:
            if len(self.stars) < 50:
                if self.loopCount % 4 == 0:
                    self.stars.append([int(random() * self.numPx), 1, [0, 0, 0]])
            else:
                print("---twinkle full")
                return State.RUNNING
        return state
