from patterns.base import PatternBase
from random import random
from neopixel import Color


class Wind(PatternBase):
    def __init__(self, numPixels):
        super(Wind, self).__init__(numPixels)

    def clear(self):
        self.wisp = []

    def newWisp(self):
        e = int(random() * 30)+10
        s = int(random() * (self.numPx-e))
        return [s, e+s, s, min(1.0, random()+0.5)]

    def _step(self, state, strip):
        for i in range(len(self.wisp)):
            if self.wisp[i][0] > self.wisp[i][1] + 1:
                strip._led_data[self.wisp[i][0]] = 0x0
                strip._led_data[self.wisp[i][0]+1] = 0x0
                if state != 3:
                    self.wisp[i] = self.newWisp()
                else:
                    del self.wisp[i]
                    if len(self.wisp) == 0:
                        print("---wind done")
                        return 0
                    break
            else:
                c = max(0, int(255.0 * ((0.5 - abs(((1.0 * self.wisp[i][1] - self.wisp[i][0])/(1.0 * self.wisp[i][1] - self.wisp[i][2])) - 0.5))*2.0)**4.0))
                strip._led_data[self.wisp[i][0] - 1] = 0x0
                strip._led_data[self.wisp[i][0]] = Color(int(c * self.wisp[i][3]/4), int(c * self.wisp[i][3]/4), c/4)
                self.wisp[i][0] += 1
                strip._led_data[self.wisp[i][0]] = Color(int(c * self.wisp[i][3]),int(c * self.wisp[i][3]), c)
                strip._led_data[self.wisp[i][0]+1] = Color(int(c * self.wisp[i][3]/4), int(c * self.wisp[i][3]/4), c/4)

        if state == 1:
            if len(self.wisp) < 20:
                if self.loopCount % 6 == 0:
                    self.wisp.append(self.newWisp())
            else:
                print("---wind full")
                return 2
        return state
