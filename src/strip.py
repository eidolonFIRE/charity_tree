from patterns.off import Off
from patterns.rainbow import Rainbow
from patterns.candycane import Candycane
from patterns.classic import Classic
from patterns.wind import Wind
from patterns.twinkle import Twinkle
from patterns.fairy import Fairy
from patterns.water_color import WaterColor

from patterns.base import State
import os


# detect OS and load visualization istead of hardware when on PC
os_type = " ".join(os.uname())
print("Current OS: %s" % os_type)
if "Raspbian" in os_type:
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
        self.rainbow = WaterColor(length)
        self.rainbow.state = State.START

        self.pats = {
            "off": Off(length),
            "rainboww": Rainbow(length),
            "candycane": Candycane(length),
            "classic": Classic(length),
            "wind": Wind(length),
            "twinkle": Twinkle(length),
            "fairy": Fairy(length),
            "watercolor": WaterColor(length),
        }

    def step(self):
        for name, pat in self.pats.items():
            if pat.state.value > State.OFF.value:
                pat.step(self.hw)
        self.hw.show()

    def solo(self, name):
        ''' start a pattern, stop all others '''
        for each in self.pats.keys():
            if name in each:
                self.pats[each].state = State.START
            else:
                if self.pats[each].state.value > State.OFF.value:
                    self.pats[each].state = State.STOP
