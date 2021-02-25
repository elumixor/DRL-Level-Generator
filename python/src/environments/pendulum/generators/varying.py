import numpy as np

from .generator import PendulumGenerator
from ..state import PendulumState


class VaryingGenerator(PendulumGenerator):
    def generate(self, difficulty: float, seed: float) -> PendulumState:
        bob_radius = 0.15
        max_angle = np.deg2rad(30)
        connector_length = 0.5
        vertical_speed = 0.02

        enemy_radius = 0.1
        enemy_x = -0.25 * seed + 0.25 * (1 - seed)
        enemy_y = 0.25

        angle = np.deg2rad(30)
        position = 0
        angular_speed = np.deg2rad(5)

        return PendulumState(bob_radius, max_angle, connector_length, vertical_speed,
                             enemy_x, enemy_y, enemy_radius,
                             angle, position, angular_speed)
