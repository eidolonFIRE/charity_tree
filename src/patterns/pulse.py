from patterns.base import base, State
from random import random, randint
from color_utils import color_wheel


class Wave():
    def __init__(self, start, end, color, speed, width):
        self.pos = start
        self.end = end
        self.color = color
        self.speed = speed
        self.width = width


class pulse(base):
    def __init__(self, strip_length):
        super(pulse, self).__init__(strip_length)
        self.num_waves = 20
        self.one_shot = True

    def clear(self):
        self.waves = []
        self.spawned = 0

    def new_wave(self):
        return Wave(
            start=0,
            end=min(self.len - 1, randint(30, self.len - 1)),
            color=color_wheel(random()),
            speed=randint(2, 5),
            width=randint(5, 15))

    def _step(self, state, leds):
        # fade all leds
        for idx in range(0, self.len):
            leds[idx] = leds[idx] * 0.8

        # render pulses
        for each in self.waves:
            for x in range(each.speed):
                leds[min(self.len - 1, each.pos + x)] = each.color
            each.pos += each.speed
            if each.pos >= each.end:
                self.waves.remove(each)

        if state == State.START:
            if self.spawned < self.num_waves:
                if randint(0, 5) == 0:
                    self.spawned += 1
                    self.waves.append(self.new_wave())
            else:
                return State.STOP
        elif state == State.STOP:
            if len(self.waves) == 0:
                return State.OFF
