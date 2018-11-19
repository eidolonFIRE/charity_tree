import numpy


def to_color(red=0.0, green=0.0, blue=0.0):
    return numpy.array([red, green, blue])


def color_blend(A, B, ratio=0.5):
    """ Weighted average of two colors.
        Note: non luminous preserving!
    """
    return A * ratio + (1.0 - ratio) * B


def color_wheel(pos, bri=1.0):
    """ Select color from rainbow
    """
    pos = pos % 1.0
    if pos < 0.333333:
        return numpy.array([pos * 3.0 * bri, (1.0 - pos * 3.0) * bri, 0.0])
    elif pos < 0.666667:
        pos -= 0.333333
        return numpy.array([(1.0 - pos * 3.0) * bri, 0.0, pos * 3.0 * bri])
    else:
        pos -= 0.666667
        return numpy.array([0.0, pos * 3.0 * bri, (1.0 - pos * 3.0) * bri])


def color_to_int(color):
    temp = color * 255.0
    return (
        (max(0, min(255, int(temp[0]))) << 16) |
        (max(0, min(255, int(temp[1]))) << 8) |
        (max(0, min(255, int(temp[2])))))
