from patterns.base import PatternBase
from random import random
from random import shuffle
from ledlib.neopixel import Color
from utils import wheel


class Fairy(PatternBase):
    def __init__(self, numPx):
        super(Fairy, self).__init__(numPx)
        self.strip_b = [random() ** 2 for x in range(numPx)]
        self.strip_c = [int(random() * 40) for x in range(numPx)]

    def clear(self):
        self.wisp = []
        self.spawn = 0

    def newWisp(self, i=-1):
        d = (int(random()*100) % 2) * 2 - 1
        length = int(random() * 15 + 8)
        px = list(range(1, length))
        c = int(random() * 1024) % 256
        return [0 if d > 0 else self.numPx - 1, d, c, length, px]

    def _step(self, state, strip):
        for i in range(len(self.wisp)):
            shuffle(self.wisp[i][4])
            if state == 3:
                if self.wisp[i][1] > 0 and self.wisp[i][0] < self.numPx / 2 or self.wisp[i][1] < 0 and self.wisp[i][0] > self.numPx / 2:
                    self.wisp[i][1] = -self.wisp[i][1]
            if self.wisp[i][0] > self.numPx + self.wisp[i][3] or self.wisp[i][0] < -self.wisp[i][3]:
                if state != 3:
                    if random() < 0.02 and self.spawn > 50:
                        self.wisp[i] = self.newWisp(i)
                        self.spawn = 0
                    self.spawn += 1
                else:
                    del self.wisp[i]
                    if len(self.wisp) == 0:
                        shuffle(self.strip_b)
                        shuffle(self.strip_c)
                        print("---fairy done")
                        return 0
                    break
            else:
                if self.wisp[i][0] - self.wisp[i][3] * self.wisp[i][1] >= 0 and self.wisp[i][0] - self.wisp[i][3] * self.wisp[i][1] < self.numPx:
                    strip._led_data[self.wisp[i][0] - self.wisp[i][3] * self.wisp[i][1]] = 0x0
                if self.wisp[i][0] >= 0 and self.wisp[i][0] < self.numPx:
                    strip._led_data[self.wisp[i][0]] = Color(255, 255, 255)
                for x in self.wisp[i][4][0:int(self.wisp[i][3]/3)]:
                    x = x * self.wisp[i][1]
                    if self.wisp[i][0] - x >= 0 and self.wisp[i][0] - x < self.numPx:
                        b = (((self.wisp[i][3]+1)-abs(x))/float(self.wisp[i][3]-1))**3 * self.strip_b[(self.wisp[i][0] + x)%self.numPx]
                        c = wheel((self.wisp[i][2] + self.strip_c[(self.wisp[i][0] + x)%self.numPx]) % 256, b)
                        strip._led_data[self.wisp[i][0] - x] = c
                self.wisp[i][0] += self.wisp[i][1]
        if state == 1:
            if len(self.wisp) < 6:
                if (self.spawn > 50 and random() < 0.1) or len(self.wisp) == 0:
                    self.wisp.append(self.newWisp())
                    self.spawn = 0
                self.spawn += 1
            else:
                print("---fairy full")
                return 2
        return state
