from base import PatternBase
from random import random


class Candycane(PatternBase):
    def __init__(self, numPixels):
        super(Candycane, self).__init__(numPixels)

    def clear(self):
        self.stripes = []

    def newStripe(self):
        r = int(random() * 5)+2  # stripe radius
        return [-r, r, int(random()*2+0.5)+1, Color(255, 0, 0) if random() < 0.5 else Color(255, 255, 255)]

    def _step(self, state, strip):
        for i in range(len(self.stripes)):
            if self.stripes[i][0] - self.stripes[i][1] > self.numPx:
                if state != 3:
                    self.stripes[i] = self.newStripe()
                else:
                    del self.stripes[i]
                    if len(self.stripes) == 0:
                        print("---candycane done")
                        return 0
                    break
            else:
                for speed in range(self.stripes[i][2] + (2 if state == 3 else 0)):
                    strip.setPixelColor(min(self.numPx, self.stripes[i][0]+self.stripes[i][1]), self.stripes[i][3])
                    strip.setPixelColor(max(0,self.stripes[i][0]-self.stripes[i][1]), 0x0)
                    self.stripes[i][0] += 1

        if state == 1:
            if len(self.stripes) < 20:
                if self.loopCount % 5 == 0:
                    self.stripes.append(self.newStripe())
            else:
                print("---candycane full")
                return 2

        return state
