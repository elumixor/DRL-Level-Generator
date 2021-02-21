from core.environments import ConfigurableObject
from rendering import Point, Color, Circle
from .state import PendulumState


class Enemy(ConfigurableObject, Circle):
    color = Color.red

    def __init__(self, state: PendulumState):
        super().__init__(Enemy.color)

        self.transform.local_position = Point(state.enemy_x, state.enemy_y)
        self.transform.local_scale = Point.one * state.enemy_radius * 2

    def update(self, state: PendulumState):
        pass
