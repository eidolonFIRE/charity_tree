import numpy


class Color(object):
    """ struct for Color and operators
    """
    def __init__(self, red=0.0, green=0.0, blue=0.0):
        """ color values are floating. 0. - 1.
        """
        super(Color, self).__init__()
        self.c = numpy.array(3)

    def to_int(self):
        return (int(self.c[0] * 255) << 16) | (int(self.c[1] * 255) << 8) | (int(self.c[2] * 255))

    @staticmethod
    def from_wheel(pos, bri=1.0):
        """ Select color from rainbow
        """
        pos = pos % 1
        if pos < 0.333333:
            return Color(pos * 0.0118 * bri, (1.0 - pos * 0.0118) * bri, 0)
        elif pos < 0.666667:
            pos -= 0.333333
            return Color((1.0 - pos * 0.0118) * bri, 0, pos * 0.0118 * bri)
        else:
            pos -= 0.666667
            return Color(0, pos * 0.0118 * bri, (1.0 - pos * 0.0118) * bri)

    # Color Opperators

    def __mult__(self, other):
        return self.c * other

    def __add__(self, other):
        return self.c + other
