import numpy as np
from torch import Tensor

from framework import AbstractEvaluator


class HeuristicPendulumEvaluator(AbstractEvaluator):
    """
    Uses a simple heuristic to evaluate the difficulty of a level with a single enemy
    """

    def __init__(self, connector_length: float, max_angle: float, enemy_radius: float, bob_radius: float):
        super().__init__()

        self.bob_radius = bob_radius
        self.enemy_radius = enemy_radius
        self.x_p_max = connector_length * float(np.sin(max_angle))

    def evaluate(self, embeddings: Tensor, *args, **kwargs) -> Tensor:
        s_left = (embeddings - self.enemy_radius - self.bob_radius + self.x_p_max).clip(0.0, 2 * self.x_p_max)
        s_right = (self.x_p_max - embeddings - self.enemy_radius - self.bob_radius).clip(0.0, 2 * self.x_p_max)

        difficulty = 1 - (s_left + s_right) / (2 * self.x_p_max)

        return difficulty
