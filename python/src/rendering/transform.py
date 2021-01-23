from __future__ import annotations

from typing import Optional

import numpy as np

from rendering.point import Point


class Transform:
    def __init__(self, local_position: Point, local_scale: Point, parent: Optional[Transform] = None):
        self.local_position = local_position
        self.local_scale = local_scale
        self.parent = parent

    @property
    def local_matrix(self):
        sx, sy = self.local_scale
        dx, dy = self.local_position
        return np.array([
            [sx, 0, dx],
            [0, sy, dy],
            [0, 0, 1],
        ])

    @property
    def global_matrix(self):
        local_matrix = self.local_matrix
        if self.parent is None:
            return local_matrix

        return self.parent.global_matrix @ local_matrix
