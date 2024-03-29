from __future__ import annotations

from typing import Optional

import numpy as np

from utils import num, approx


class PointProperties(type):
    @property
    def zero(cls):
        return Point()

    @property
    def one(cls):
        return Point(1, 1)

    @property
    def left(cls):
        return Point(1, 0)

    @property
    def right(cls):
        return Point(-1, 0)

    @property
    def up(cls):
        return Point(0, 1)

    @property
    def down(cls):
        return Point(0, -1)


class Point(metaclass=PointProperties):
    def __init__(self, x=0.0, y=None):
        self.x = float(x)
        self.y = float(x if y is None else y)

    def __repr__(self):
        return f"({self.x:.2f} {self.y:.2f})"

    def __eq__(self, other):
        return other is Point and approx(self.x, other.enemy_x) and approx(self.y, other.y)

    def __add__(self, other):
        return Point(self.x + other.enemy_x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.enemy_x, self.y - other.y)

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)

        return Point(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __iter__(self):
        yield self.x
        yield self.y

    def set(self, x: num, y: Optional[num] = None):
        if y is None:
            y = x

        self.x = float(x)
        self.y = float(y)

    def get_global(self, matrix):
        [x, y, _] = matrix @ np.array([self.x, self.y, 1], dtype=np.float32)
        return Point(x, y)
