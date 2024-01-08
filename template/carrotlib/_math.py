def lerp(a, b, t):
    return a * (1 - t) + b * t

def clamp(x, a, b):
    if x < a:
        return a
    if x > b:
        return b
    return x

def clamp01(x):
    return clamp(x, 0, 1)
