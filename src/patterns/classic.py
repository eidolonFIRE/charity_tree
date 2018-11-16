from patterns.base import base, State
from random import random
from random import shuffle
from utils import to_color


class classic(base):
    def __init__(self, numPixels):
        numPixels = numPixels - (numPixels % 4)   # makes sure that numPixels can be divided by 4, e.g, numPixels = 150 wouldn't work 
        super(classic, self).__init__(numPixels)
        self.strip_order = list(range(0, numPixels, 4))
        shuffle(self.strip_order)

    def clear(self):
        self.dots = []

    def newDot(self, strip, idx):
        x = self.strip_order[idx] + (int(random() * 100) % 4)
        if random() > 0.05 and idx < len(self.dots):
            x = self.dots[idx][0]
        strip.setPixelColor(x, to_color(255, 240, 100))
        return [x, int(random() * 100)]

    def _step(self, state, strip):
        for i in range(len(self.dots)):
            if self.dots[i][1] == 0:
                strip.setPixelColor(self.dots[i][0], 0x0)
                if state != State.STOP:
                    self.dots[i] = self.newDot(strip, i)
                else:
                    del self.dots[i]
                    if len(self.dots) == 0:
                        shuffle(self.strip_order)
                        print("---classic done")
                        return State.OFF
                    break
            else:
                self.dots[i][1] -= 1
        if state == State.START:
            if len(self.dots) < len(self.strip_order):
                self.dots.append(self.newDot(strip, len(self.dots)))
            else:
                print("---classic full")
                return State.RUNNING
        return state
