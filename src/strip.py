from patterns.off import Off
from patterns.rainbow import Rainbow
from patterns.candycane import Candycane
from patterns.classic import Classic
from patterns.wind import Wind
from patterns.twinkle import Twinkle
from patterns.fairy import Fairy
from patterns.water_color import WaterColor

from ledlib.neopixel import Adafruit_NeoPixel, ws


class Strip(object):
    """   """
    def __init__(self, length, pin, dma, channel):
        super(Strip, self).__init__()
        self.length = length
        self.hw = Adafruit_NeoPixel(length, pin=pin, dma=dma, channel=channel, strip_type=ws.WS2811_STRIP_GRB)
        self.hw.begin()
        self.rainbow = Fairy(length)
        self.rainbow.state = 1

    def step(self):
        self.rainbow.state = self.rainbow.step(self.hw)
        self.hw.show()
