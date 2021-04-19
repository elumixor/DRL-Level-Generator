from __future__ import annotations

import numpy as np

from rendering.point import Point
from utils import approx


class Transform:
    def __init__(self, local_position: Point = Point.zero, local_scale: Point = Point.one, rotation: float = 0.0):
        self.local_position = local_position
        self.local_scale = local_scale
        self.rotation = rotation

    @property
    def local_matrix(self):
        sx, sy = self.local_scale
        dx, dy = self.local_position

        scale_translate = np.array([
            [sx, 0, dx],
            [0, sy, dy],
            [0, 0, 1],
        ], dtype=np.float32)

        if approx(self.rotation % (2 * np.pi), 0.0):
            return scale_translate

        else:
            cos = np.cos(self.rotation)
            sin = np.sin(self.rotation)

            rotate = np.array([
                [cos, -sin, 0],
                [sin, cos, 0],
                [0, 0, 1],
            ])

            return scale_translate @ rotate
