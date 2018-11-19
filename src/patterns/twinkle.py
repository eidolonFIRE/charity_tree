from patterns.base import base, State
from random import random, randint
from color_utils import to_color


class Star():
    def __init__(self, pos, state, color):
        self.pos = pos
        self.state = state
        self.color = color


class twinkle(base):
    def __init__(self, strip_length):
        super(twinkle, self).__init__(strip_length)

    def clear(self):
        self.stars = []
        self.num_stars = 30

    def _step(self, state, leds):
        for i, x in enumerate(self.stars):
            if x.state == 0:
                # dimming
                if sum(x.color) < 0.1:
                    if state == State.STOP:
                        self.stars.remove(x)
                        if len(self.stars) == 0:
                            return State.OFF
                        break
                    else:
                        while True:
                            idx = randint(0, self.len - 1)
                            flag = False
                            for each in self.stars:
                                if idx == each.pos:
                                    break
                            if not flag:
                                break
                        x.pos = idx
                        x.state = 1
                else:
                    x.color *= 0.9
            else:
                # brightening
                if sum(x.color) > 2.9:
                    x.state = 0
                else:
                    x.color = to_color(*[min(1.0, c + (random()**3)/10.0) for c in x.color])
            leds[x.pos] = x.color
        if state == State.START:
            if len(self.stars) < self.num_stars:
                if self.loopCount % 5 == 0:
                    self.stars.append(Star(randint(0, self.len - 1), 1, to_color()))
            else:
                return State.RUNNING
        return state
