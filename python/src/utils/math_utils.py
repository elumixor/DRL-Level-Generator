from random import random


def approx(a: float, b: float, eps=1e-7):
    return abs(a - b) < eps


def mean(iterable):
    return sum(iterable) / len(iterable)


def sign(x):
    return -x if random() < 0.5 else x


def clamp(value, _min, _max):
    return max(_min, min(value, _max))
