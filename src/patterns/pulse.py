from patterns.base import base, State
from random import randint
from utils import wheel, mult_color


class Wave():
    def __init__(self, start, end, color, speed, width):
        self.pos = start
        self.end = end
        self.color = color
        self.speed = speed
        self.width = width


class pulse(base):
    def __init__(self, numPixels):
        super(pulse, self).__init__(numPixels)
        self.num_waves = 4
        self.one_shot = True

    def clear(self):
        self.waves = []
        self.spawned = 0

    def new_wave(self):
        return Wave(
            start=0,
            end=min(self.numPx - 1, randint(30, self.numPx - 1)),
            color=wheel(randint(0, 255)),
            speed=randint(1, 3),
            width=randint(5, 15))

    def _step(self, state, strip):
        # fade whole strip
        for idx in range(0, self.numPx):
            strip._led_data[idx] = mult_color(strip._led_data[idx], 0.9)

        # render pulses
        for each in self.waves:
            for x in range(each.speed):
                strip._led_data[min(self.numPx - 1, each.pos + x)] = each.color
            each.pos += each.speed
            if each.pos >= each.end:
                self.waves.remove(each)

        if state == State.START:
            if self.spawned < self.num_waves:
                self.spawned += 1
                self.waves.append(self.new_wave())
            else:
                state = State.STOP
        elif state == State.STOP:
            if len(self.waves) == 0:
                state = State.OFF
        return state
