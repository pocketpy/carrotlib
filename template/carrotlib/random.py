from math import cos, log, exp, sqrt
from random import random

def poisson(lam: float) -> int:
    """This function has performance issue when `lam >= 10`"""
    if lam == 0:
        return 0
    enlam = exp(-lam)
    X = 0
    prod = 1.0
    while True:
        U = random()
        prod *= U
        if prod > enlam:
            X += 1
        else:
            return X
        
def binomial(n: int, p: float) -> int:
    if p >= 1:
        return n
    X = 0
    for _ in range(n):
        if random() < p:
            X += 1
    return X

def normal(mu: float, sigma: float) -> float:
    u1 = random()
    u2 = random()
    z = (cos(2 * 3.141592653589793 * u2) * sqrt(-2 * log(u1)))
    return mu + sigma * z
