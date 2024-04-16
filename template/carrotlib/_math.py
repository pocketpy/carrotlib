def lerp(a, b, t):
    """Linearly interpolate between two values.
    Equivalent to `a + (b - a) * t`.
    """
    return a + (b - a) * t

def clamp(x, a, b):
    """Clamp a value between `a` and `b`."""
    if a > b: a, b = b, a
    if x < a: return a
    if x > b: return b
    return x

def clamp01(x):
    """Clamp a value between 0 and 1."""
    return clamp(x, 0, 1)
