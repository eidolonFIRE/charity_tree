from patterns.base import base, State


class filter_blur(base):
    def __init__(self, strip_length):
        super(filter_blur, self).__init__(strip_length)
        self.radius = 2
        self.one_shot = True

    def _step(self, state, leds):
        for idx in range(0, self.len):
            denominator = (self.radius * 2 + 1) - min(0, idx - self.radius) - min(0, self.len - idx)
            leds[idx] = sum(leds[max(0, idx - self.radius):min(self.len, idx + self.radius + 1)]) / denominator

        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF
        else:
            return state
