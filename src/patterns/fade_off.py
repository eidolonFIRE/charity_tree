from patterns.base import base, State


class fade_off(base):
    def __init__(self, strip_length):
        super(fade_off, self).__init__(strip_length)

    def _step(self, state, leds):
        for idx in range(self.len - 1):
            leds[idx] = leds[idx] * 0.9 + leds[idx + 1] * 0.05
        leds[self.len - 1] *= 0.9

        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF
