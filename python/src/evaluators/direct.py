import numpy as np


class DirectEvaluator:
    def __init__(self, connector_length, max_angle, enemy_radius, bob_radius):
        self.bob_radius = bob_radius
        self.enemy_radius = enemy_radius
        self.x_p_max = connector_length * np.sin(max_angle)

    def evaluate(self, x):
        s_left = (x - self.enemy_radius - self.bob_radius + self.x_p_max).clip(0.0, 2 * self.x_p_max)
        s_right = (self.x_p_max - x - self.enemy_radius - self.bob_radius).clip(0.0, 2 * self.x_p_max)

        return 1 - (s_left + s_right) / (2 * self.x_p_max)
