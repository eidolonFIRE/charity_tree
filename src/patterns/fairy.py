from patterns.base import base, State
from random import random, shuffle, randint
from color_utils import to_color, color_wheel


class Wisp():
    def __init__(self, strip_length):
        self.length = randint(10, 30)
        self.px = list(range(1, self.length))
        self.color = random()
        self.dir = randint(0, 1) * 2 - 1
        self.pos = 0 if self.dir == 1 else strip_length - 1


class fairy(base):
    def __init__(self, strip_length):
        self.strip_b = [random() ** 2 for x in range(strip_length)]
        self.strip_c = [random() / 4.0 for x in range(strip_length)]
        self.num_wisps = 4
        super(fairy, self).__init__(strip_length)

    def clear(self):
        self.wisps = []
        shuffle(self.strip_c)
        shuffle(self.strip_b)

    def _step(self, state, leds):
        for wisp in self.wisps:
            shuffle(wisp.px)
            # check if wisp needs to turn back toward nearest end of the led stirp
            if state == State.STOP:
                if wisp.dir > 0 and wisp.pos < self.len / 2 or wisp.dir < 0 and wisp.pos > self.len / 2:
                    wisp.dir = -wisp.dir
            # check wisp finished
            if wisp.pos > self.len + wisp.length or wisp.pos < -wisp.length:
                self.wisps.remove(wisp)
                if state == State.STOP and len(self.wisp) == 0:
                    return State.OFF
            else:
                # clear tail
                if wisp.pos - wisp.length * wisp.dir >= 0 and wisp.pos - wisp.length * wisp.dir < self.len:
                    leds[wisp.pos - wisp.length * wisp.dir] = to_color()
                # white leading spark
                if wisp.pos >= 0 and wisp.pos < self.len:
                    leds[wisp.pos] = to_color(1.0, 1.0, 1.0)
                # sparkly tail
                for x in wisp.px[0:int(wisp.length/3)]:
                    x = x * wisp.dir
                    if wisp.pos - x >= 0 and wisp.pos - x < self.len:
                        b = (((wisp.length + 1) - abs(x)) / float(wisp.length - 1))**2 * self.strip_b[(wisp.pos + x) % self.len]
                        leds[wisp.pos - x] = color_wheel(wisp.color + self.strip_c[(wisp.pos + x) % self.len], b)
                # incr move wisp
                wisp.pos += wisp.dir

        # spawning in new wisps
        if state == State.START:
            state = State.RUNNING
        if state == State.RUNNING:
            if len(self.wisps) < self.num_wisps and randint(0, 20) == 0:
                self.wisps.append(Wisp(self.len))
        return state
