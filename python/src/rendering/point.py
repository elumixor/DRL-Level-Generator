from __future__ import annotations

import numpy as np

from utilities import approx


class Point:
    def __init__(self, x=0.0, y=None):
        self._x = float(x)
        self._y = float(x if y is None else y)
        self._arr = np.array([x, y, 1])

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __repr__(self):
        return f"({self._x:.2f} {self._y:.2f}"

    def __eq__(self, other):
        return other is Point and approx(self._x, other.x) and approx(self._y, other.y)

    def __add__(self, other):
        return Point(self._x + other.x, self._y + other.y)

    def __sub__(self, other):
        return Point(self._x - other.x, self._y - other.y)

    def __abs__(self):
        return Point(abs(self._x), abs(self._y))

    def __iter__(self):
        yield self._x
        yield self._y

    def get_global(self, matrix):
        [x, y, _] = matrix @ self._arr
        return Point(x, y)
