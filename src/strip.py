import importlib
from patterns.base import State
import os

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


class Strip(object):
    """   """
    def __init__(self, length, pin, dma, channel):
        super(Strip, self).__init__()
        self.length = length
        self.hw = Adafruit_NeoPixel(length, pin=pin, dma=dma, channel=channel, strip_type=ws.WS2811_STRIP_GRB)
        self.hw.begin()
        self.pats = {}

        # init an instance of each pattern
        for key, value in pattern_classes.items():
            self.pats[key] = value(length)

    def step(self):
        for name, pat in self.pats.items():
            if pat.state.value > State.OFF.value:
                pat.step(self.hw)
        self.hw.show()

    def solo(self, name):
        ''' start a pattern, stop all others '''
        for each in self.pats.keys():
            if name == each:
                self.pats[each].state = State.START
            else:
                if self.pats[each].state.value > State.OFF.value:
                    self.pats[each].state = State.STOP
