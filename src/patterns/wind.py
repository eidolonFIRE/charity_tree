from patterns.base import base, State
from random import randint, random
from color_utils import to_color


class Wisp():
    def __init__(self, strip_length):
        self.length = randint(10, 40)
        self.pos = randint(0, strip_length - self.length - 2)
        self.start = self.pos
        self.end = self.pos + self.length
        self.intensity = random()


class wind(base):
    def __init__(self, strip_length):
        super(wind, self).__init__(strip_length)
        self.num_wisps = 10

    def clear(self):
        self.wisps = []

    def _step(self, state, leds):
        for each in self.wisps:
            if each.pos > each.end:
                leds[each.pos - 1] = to_color()
                leds[each.pos] = to_color()
                if state != State.STOP:
                    self.wisps.append(Wisp(self.len))
                else:
                    if len(self.wisps) == 0:
                        return State.OFF
                self.wisps.remove(each)
            else:
                c = max(0, ((0.5 - abs((float(each.pos - each.start) / each.length) - 0.5)) * 2.0)**2.0)
                leds[each.pos - 1] = to_color()
                leds[each.pos + 0] = to_color(1.0, 1.0, 1.0) * c * each.intensity / 3
                if each.pos + 1 < self.len:
                    leds[each.pos + 1] = to_color(1.0, 1.0, 1.0) * c * each.intensity
                if each.pos + 2 < self.len:
                    leds[each.pos + 2] = to_color(1.0, 1.0, 1.0) * c * each.intensity / 3

        if state == State.START:
            if len(self.wisps) < self.num_wisps:
                if self.loopCount % 6 == 0:
                    self.wisps.append(Wisp(self.len))
            else:
                return State.RUNNING
        return state
