from enum import Enum
import pygame


class ws(Enum):
    WS2811_STRIP_GRB = 0


class Adafruit_NeoPixel_stub(object):
    """docstring for Adafruit_NeoPixel_stub"""
    def __init__(self, length, pin, dma, channel, strip_type):
        super(Adafruit_NeoPixel_stub, self).__init__()
        self.length = length
        self.pin = pin
        self.dma = dma
        self.channel = channel
        self.strip_type = strip_type
