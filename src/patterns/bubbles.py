from patterns.base import base, State
from random import random, randint
from color_utils import color_wheel, to_color


class Bub():
    def __init__(self, strip_length):
        self.color = color_wheel(random())
        self.radius = randint(3, 15)
        self.cur_radius = 0.0
        self.pos = randint(self.radius, strip_length - self.radius - 1)
        self.state = 0.2

    def step(self):
        """ return True if bubble is end-of-life
        """
        self.cur_radius += self.state
        if self.cur_radius >= self.radius:
            self.state = -0.5
        elif self.cur_radius < 0:
            return True
        return False

    def render(self, leds):
        # draw center color
        for x in range(int(-self.cur_radius), int(self.cur_radius + 1)):
            leds[self.pos + x] = self.color
        # clear edges
        if self.state < 0:
            leds[int(self.pos + self.cur_radius)] = to_color()
            leds[int(self.pos - self.cur_radius)] = to_color()


class bubbles(base):
    def __init__(self, strip_length):
        super(bubbles, self).__init__(strip_length)
        self.num_bubs = 20
        self.one_shot = True

    def clear(self):
        self.waves = []
        self.spawned = 0

    def _step(self, state, leds):
        # process bubbles
        for each in self.waves:
            each.render(leds)
            if each.step():
                self.waves.remove(each)

        # state machine
        if state == State.START:
            if self.spawned < self.num_bubs:
                if randint(0, 10) == 0:
                    self.spawned += 1
                    self.waves.append(Bub(self.len))
            else:
                return State.STOP
        elif state == State.STOP:
            if len(self.waves) == 0:
                return State.OFF
