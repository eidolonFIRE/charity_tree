
def to_color(red, green, blue, white=0):
    """ Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
    """
    return (int(white) << 24) | (int(red) << 16) | (int(green) << 8) | int(blue)

def color_to_tuple(color):
    return ((color >> 16) & 0xff,  (color >> 8) & 0xff, color & 0xff)

def mult_color(color, bri):
    """ Multiply a color by a brightness factor  0. to 1.
    """
    r, g, b = color_to_tuple(color)
    return to_color(r * bri, g * bri, b * bri)

def blend_color(A, B, ratio):
    """ Weighted average of two colors.
        Note: non luminous preserving!
    """
    ar, ag, ab = color_to_tuple(A)
    br, bg, bb = color_to_tuple(B)
    i_ratio = 1.0 - ratio
    return to_color(ar * ratio + br * i_ratio, ag * ratio + bg * i_ratio, ab * ratio + bb * i_ratio)

def wheel(pos, bri=1):
    """ Generate rainbow colors across 0-255 positions.
    """
    pos = int(pos) % 256
    if pos < 85:
        return to_color( pos * 3 *bri, (255 - pos * 3) * bri, 0)
    elif pos < 170:
        pos -= 85
        return to_color((255 - pos * 3) * bri, 0, pos * 3 * bri)
    else:
        pos -= 170
        return to_color(0, pos * 3 * bri, (255 - pos * 3) * bri)
