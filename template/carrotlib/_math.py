def lerp(a, b, t):
    return a + (b - a) * t

def clamp(x, a, b):
    if a > b: a, b = b, a
    if x < a: return a
    if x > b: return b
    return x

def clamp01(x):
    return clamp(x, 0, 1)
