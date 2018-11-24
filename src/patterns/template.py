from patterns.base import base, State
from random import random, shuffle
from color_utils import to_color, color_blend, color_wheel

#
# WARN: Class name must be the same as the file name!
#
class template(base):
    def __init__(self, strip_length):
        self.strip_order = list(range(strip_length))
        super(template, self).__init__(strip_length)

    def clear(self):
        '''
            Gets called when pattern is initiated or reset.
        '''
        self.i = 0
        shuffle(self.strip_order)

    def _step(self, state, leds):
        '''
            This is called each frame of the main loop.

            state: current state of the pattern. See base.py -> State(Enum)
            leds: hw access to leds
        '''

        # === sample method 1
        # Iter through all leds in a random order.
        # Each time we enter this _step we're only updating 1 led.
        # This is nice for high cost patterns.
        if self.i >= len(self.strip_order):
            self.i = 0
            shuffle(self.strip_order)
            # state machine only updates when we've visited every led at least once.
            if state == State.START:
                return State.RUNNING
            elif state == State.STOP:
                return State.OFF
        # set led to random color
        leds[self.strip_order[self.i]] = color_wheel(random())
        self.i += 1

        # === sample method 2
        # Update all leds every frame.
        # This is do-able for low cost patterns.
        for i in range(self.len):
            leds[i] = wheel(random())
        # Instantly update state machine.
        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF


        # Instantly update state machine.
        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF

        # === other examples  (see utils.py for more useful functions)

        # select a random LED
        index = randint(0, self.len - 1)

        # set that LED to white
        leds[index] = to_color(1.0, 1.0, 1.0)

        # set that LED to a random color dimmed by half
        leds[index] = color_wheel(random) * 0.5

        # set that LED to blend between white and red
        leds[index] = color_blend(to_color(1.0, 0.0, 0.0), to_color(1.0, 1.0, 1.0), 0.5)
