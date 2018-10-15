from patterns.base import PatternBase
from random import random
from random import shuffle

from utils import wheel


class WaterColor(PatternBase):
    def __init__(self, numPixels):
        super(WaterColor, self).__init__(numPixels)
        self.strip_order = list(range(numPixels))
        shuffle(self.strip_order)
        self.buff = [0] * numPixels
        self.full_stop = True

    def clear(self):
        self.i = 0
        self.cleared = 0
        self.baseC = int(random()*1024) % 256
        self.dots = []  # [self.newDot() for x in range(15)]

    def newDot(self):
        return [int(random()*900) % self.numPx, wheel((self.baseC + int(random() * 40)) % 256, random()**2)]

    def _step(self, state, strip):
        if state == 1:
            self.buff = strip._led_data
            print("---waterColor full")
            return 2
        for t in range(40):
            if self.i >= len(self.strip_order):
                self.i = 0
                shuffle(self.strip_order)
            if self.i == 0 and state == 3:
                if self.cleared == 2:
                    self.cleared = 0
                    print("---waterColor done")
                    return 0
                self.cleared += 1
            pos = self.strip_order[self.i]
            if state != 3:
                c0 = self.buff[pos-1]
                # c1 = self.buff[pos]
                c2 = self.buff[(pos+1)%self.numPx]
                c = ((((c0&0xff0000)+(c2&0xff0000))>>1) & 0xff0000) |\
                    ((((c0&  0xff00)+(c2&  0xff00))>>1) & 0xff00) |\
                    ((((c0&    0xff)+(c2&    0xff))>>1) & 0xff)
                self.buff[pos] = c
            else:
                self.buff[pos] = 0
            self.i += 1
        if state != 3:
            # update base dots
            for t in self.dots:
                self.buff[t[0]] = t[1]
            # add dots
            if len(self.dots) < 10 and self.loopCount % 10 == 0:
                self.dots.append(self.newDot())
            # base color
            if self.loopCount % 10 == 0:
                i = int(random()*1000) % len(self.dots)
                self.dots[i] = self.newDot()
            # color burst
            if self.loopCount % 30 == 0:
                c = wheel(int(random()*1024) % 256)
                i = int(random()*900) % (self.numPx-4)
                self.buff[i:i+4] = [c]*4
            # change base color
            if self.loopCount % 100 == 0 and random() < 0.1:
                self.baseC = int(random()*1024) % 256
                print("---waterColor base color change %d" % self.baseC)
        return state
