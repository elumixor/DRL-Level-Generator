from __future__ import annotations

import numpy as np

from rendering.point import Point


class Transform:
    def __init__(self, local_position: Point, local_scale: Point):
        self.local_position = local_position
        self.local_scale = local_scale

    @property
    def local_matrix(self):
        sx, sy = self.local_scale
        dx, dy = self.local_position
        return np.array([
            [sx, 0, dx],
            [0, sy, dy],
            [0, 0, 1],
        ], dtype=np.float32)
