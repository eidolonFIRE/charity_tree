from patterns.base import base, State
from random import random, randint, shuffle
from utils import wheel, blend_color


class watercolor(base):
    def __init__(self, numPixels):
        super(watercolor, self).__init__(numPixels)
        self.strip_order = list(range(numPixels))
        shuffle(self.strip_order)
        self.full_stop = True

    def clear(self):
        self.i = 0
        self.cleared = 0
        self.baseC = int(random()*1024) % 256
        self.dots = []

    def newDot(self):
        return [randint(0, self.numPx - 1), wheel(self.baseC + random() * 30, random())]

    def _step(self, state, strip):
        if state == State.START:
            return State.RUNNING
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
            if state != State.STOP:
                # c0 = strip._led_data[pos-1]
                # c1 = strip._led_data[pos]
                # c2 = strip._led_data[(pos+1)%self.numPx]
                # c = ((((c0&0xff0000)+(c2&0xff0000))>>1) & 0xff0000) |\
                #     ((((c0&  0xff00)+(c2&  0xff00))>>1) & 0xff00) |\
                #     ((((c0&    0xff)+(c2&    0xff))>>1) & 0xff)
                strip._led_data[pos] = blend_color(strip._led_data[pos-1], strip._led_data[(pos+1)%self.numPx], 0.5)
            else:
                strip._led_data[pos] = 0
            self.i += 1
        if state != State.STOP:
            # update base dots
            for t in self.dots:
                strip._led_data[t[0]] = t[1]
            # add dots
            if len(self.dots) < 6 and self.loopCount % 10 == 0:
                self.dots.append(self.newDot())
            # base color
            if self.loopCount % 10 == 0:
                i = randint(0, len(self.dots) - 1)
                self.dots[i] = self.newDot()
            # color burst
            if self.loopCount % 20 == 0:
                c = wheel(randint(0, 255))
                i = randint(0, self.numPx - 5)
                strip._led_data[i:i+4] = [c]*4
            # change base color
            if self.loopCount % 100 == 0 and randint(0, 9) == 0:
                self.baseC = randint(0, 255)
        return state
