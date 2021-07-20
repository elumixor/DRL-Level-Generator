import numpy as np
from torch import Tensor

from framework import AbstractEvaluator
from pendulum import PendulumState


class HeuristicPendulumEvaluator(AbstractEvaluator):
    """
    Uses a simple heuristic to evaluate the difficulty of a level with a single enemy
    """

    def __init__(self, connector_length: float, max_angle: float, enemy_radius: float, bob_radius: float):
        super().__init__()

        self.bob_radius = bob_radius
        self.enemy_radius = enemy_radius
        self.x_p_max = connector_length * float(np.sin(max_angle))

    def evaluate(self, embeddings: PendulumState) -> Tensor:
        x = embeddings.enemy_x

        s_left = (x - self.enemy_radius - self.bob_radius + self.x_p_max).clip(0.0, 2 * self.x_p_max)
        s_right = (self.x_p_max - x - self.enemy_radius - self.bob_radius).clip(0.0, 2 * self.x_p_max)

        return 1 - (s_left + s_right) / (2 * self.x_p_max)
