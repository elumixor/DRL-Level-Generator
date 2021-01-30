import numpy as np


class ColorProperties(type):
    @property
    def black(cls):
        return Color()

    @property
    def white(cls):
        return Color(1, 1, 1)

    @property
    def transparent(cls):
        return Color(a=0)

    @property
    def red(cls):
        return Color(r=1)

    @property
    def green(cls):
        return Color(g=1)

    @property
    def blue(cls):
        return Color(b=1)


class Color(metaclass=ColorProperties):
    def __init__(self, r: float = 0, g: float = 0, b: float = 0, a: float = 1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @property
    def to_numpy(self):
        return np.array([self.r, self.g, self.b, self.a], dtype=np.float32)
