from patterns.base import base, State
from random import randint, shuffle
from utils import to_color, color_to_tuple, mult_color, blend_color, wheel

#
# WARN: Class name must be the same as the file name!
#
class template(base):
    def __init__(self, numPixels):
        super(template, self).__init__(numPixels)

    def clear(self):
        '''
            Gets called when pattern is initiated or reset.
        '''
        self.i = 0

    def _step(self, state, strip):
        '''
            This is called each frame of the main loop.

            state: current state of the pattern. See base.py -> State(Enum)
            strip: hw access to leds
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
        strip.setPixelColor(self.strip_order[self.i], wheel(randint(0, 255)))
        self.i += 1

        # === sample method 2
        # Update all leds every frame.
        # This is do-able for low cost patterns.
        for i in range(self.numPx):
            strip.setPixelColor(i, wheel(randint(0, 255)))
        # Instantly update state machine.
        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF

        # === sample method 3
        # Similar to #2 but using list comprehension and more direct access.
        strip._led_data = [wheel(randint(0, 255)) for x in range(self.numPx)]

        # Instantly update state machine.
        if state == State.START:
            return State.RUNNING
        elif state == State.STOP:
            return State.OFF

        # === other examples

        # select a random LED
        index = randint(0, self.numPx - 1) 

        # set that LED to white
        strip.setPixelColor(index, to_color(255, 255, 255))

        # set that LED to a random color dimmed by half
        strip.setPixelColor(index, mult_color(wheel(randint(0, 255)), 0.5))

        # set that LED to blend between white and red
        strip.setPixelColor(index, blend_color(to_color(255, 0, 0), to_color(255, 255, 255), 0.5))

        # ===
        # Updated state must always be returned here.
        return state
