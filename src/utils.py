
def color(red, green, blue, white=0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return (white << 24) | (red << 16) | (green << 8) | blue


def wheel(pos, bri=1):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(int((pos * 3)*bri), int((255 - pos * 3) * bri), 0)
    elif pos < 170:
        pos -= 85
        return Color(int((255 - pos * 3) * bri), 0, int(pos * 3 * bri))
    else:
        pos -= 170
        return Color(0, int(pos * 3 * bri), int((255 - pos * 3) * bri))
