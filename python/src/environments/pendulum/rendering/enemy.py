import numpy as np

from rendering import Point, Color, Circle
from ..state import enemy_x, enemy_y, enemy_radius


class Enemy(Circle):
    color = Color.red

    def __init__(self, state: np.ndarray):
        super().__init__(Enemy.color)
        self.update(state)

    def update(self, state):
        self.transform.local_position = Point(state[enemy_x], state[enemy_y])
        self.transform.local_scale = Point.one * state[enemy_radius] * 2
