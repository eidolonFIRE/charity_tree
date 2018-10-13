
def wheel(pos, bri = 1):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(int((pos * 3)*bri), int((255 - pos * 3) * bri), 0)
    elif pos < 170:
        pos -= 85
        return Color(int((255 - pos * 3) * bri), 0, int(pos * 3 * bri))
    else:
        pos -= 170
        return Color(0, int(pos * 3 * bri), int((255 - pos * 3) * bri))
