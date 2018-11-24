from patterns.base import base, State
from color_utils import to_color
from random import randint


class Stripe():
    def __init__(self):
        self.length = randint(4, 12)
        self.pos = 0
        self.color = to_color(1.0, 0, 0) if randint(0, 1) else to_color(1.0, 1.0, 1.0)


class burst(base):
    def __init__(self, strip_length):
        self.num_stripes = 10
        super(burst, self).__init__(strip_length)

    def clear(self):
        self.stripes = []

    def _step(self, state, leds):
        for each in self.stripes:
            if each.pos - each.length > self.len:
                self.stripes.remove(each)
                if state != State.STOP:
                    self.stripes.append(Stripe())
                else:
                    if len(self.stripes) == 0:
                        return State.OFF
            else:
                speed = 4 if state == State.STOP else 2
                for rep in range(speed):
                    # clear tail
                    leds[min(self.len - 1, max(0, each.pos - each.length))] = to_color()

                    # set leader
                    if each.pos < self.len:
                        leds[each.pos] = each.color

                    # move stripe
                    each.pos += 1

        if state == State.START:
            if len(self.stripes) < self.num_stripes:
                if randint(0, 5) == 0:
                    self.stripes.append(Stripe())
            else:
                return State.RUNNING
