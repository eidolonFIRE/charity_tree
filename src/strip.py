import importlib
from patterns.base import State
import os
from color import Color

# detect and load patterns
pattern_files = [f.replace(".py", "") for f in os.listdir("patterns") if os.path.isfile(os.path.join("patterns", f))]
pattern_classes = {}
print("Importing Patterns:")
for name in pattern_files:
    print("    - %s" % name)
    globals()[name] = importlib.import_module("patterns." + name, package=None)
    pattern_classes[name] = globals()[name].__dict__[name]

# detect OS and load visualization istead of hardware when on PC
os_type = " ".join(os.uname())
print("Current OS: %s" % os_type)
if "raspberrypi" in os_type:
    print("Loading on Raspberry pi, using pwm hardware.")
    from ledlib.neopixel import Adafruit_NeoPixel, ws
else:
    print("Loading on dev PC, using stub visualization.")
    from stub import Adafruit_NeoPixel_stub as Adafruit_NeoPixel, ws


class HwInter(object):
    """ Hardware interface
    """
    def __init__(self, length, pin, dma, channel):
        super(HwInter, self).__init__()
        self._hw = Adafruit_NeoPixel(length, pin=pin, dma=dma, channel=channel, strip_type=ws.WS2811_STRIP_GRB)
        self._hw.begin()
        self.length = length
        self.buffer = [Color()] * length

    def flush(self):
        """ Flush buffer to strip
        """
        for x in range(self.length):
            self._hw._led_data[x] = self.buffer[x].to_int()
        self._hw.show()


class Strip(object):
    """   """
    def __init__(self, length, pin, dma, channel):
        super(Strip, self).__init__()
        self.length = length
        self.hw = HwInter(length, pin, dma, channel)
        self.pats = {}

        # new instance of each pattern
        for key, value in pattern_classes.items():
            self.pats[key] = value(length)

    def step(self):
        for name, pat in self.pats.items():
            if pat.state.value > State.OFF.value:
                pat.step(self.hw)
        self.hw.flush()

    def solo(self, name):
        ''' start a pattern, stop all others '''
        if name in self.pats.keys():
            # start the desired pattern
            self.pats[name].state = State.START
            if not self.pats[name].one_shot:
                # stop all other patterns
                for each in self.pats.keys():
                    if name != each and self.pats[each].state.value > State.OFF.value:
                        self.pats[each].state = State.STOP
        else:
            print("Unknown pattern \"%s\"" % name)
