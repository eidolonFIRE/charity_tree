from patterns.base import base, State
from random import randint
from color_utils import to_color


class Dot():
    def __init__(self, pos):
        self.pos = pos
        self.offset = randint(0, 3)
        self.color = to_color()
        self.life = randint(0, 20)

    def reset(self):
        self.offset = randint(0, 3)
        self.color = to_color(1.0, 0.9, 0.6)
        self.life = randint(100, 1000)


class classic(base):
    def __init__(self, strip_length):
        super(classic, self).__init__(strip_length)

    def clear(self):
        self.dots = [Dot(x * 4) for x in range(int(self.len / 4))]

    def _step(self, state, leds):
        for each in self.dots:
            each.life -= 5 if state == State.STOP else 1
            if each.life <= 0:
                if state != State.STOP:
                    # clear old led and set to new one
                    leds[each.pos + each.offset] = to_color()
                    each.reset()
                else:
                    # check if empty
                    self.dots.remove(each)
                    if len(self.dots) == 0:
                        return State.OFF
            # draw current led
            leds[each.pos + each.offset] = each.color

        if state == State.START:
            return State.RUNNING
