from __future__ import annotations

import numpy as np

from rendering.game_object import GameObject


class CircleCollider:
    def __init__(self, radius: float, game_object: GameObject):
        self.game_object = game_object
        self.radius = radius

    def collides_with(self, other: CircleCollider):
        center_self = self.game_object.global_center
        center_other = other.game_object.global_center

        return np.linalg.norm(center_self - center_other) < (self.radius + other.radius)
