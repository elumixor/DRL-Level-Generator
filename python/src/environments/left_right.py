from random import random
from typing import Tuple, Any

import numpy as np

from environments import BaseEnvironment
from utilities import DotDict


class LeftRightEnvironment(BaseEnvironment):

    @property
    def action_size(self):
        return DotDict(n=2)

    @property
    def observation_size(self):
        return np.array([1])

    def __init__(self, positions=(-5, 5), rewards=(10, 5, -1), spawn_positions=(-0, 3), step_distance=1):
        self.spawn_positions = spawn_positions
        self.rewards = rewards
        self.positions = positions
        self.step_distance = step_distance
        self.position = np.array(0)

    def reset(self) -> np.ndarray:
        big_position, small_position = self.spawn_positions
        self.position = np.array([random() * (small_position - big_position) + big_position])
        return self.position

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, Any]:
        """
        :param action: If 0 go left, 1 go right
        """
        direction = np.array([-1 if action < .5 else 1])

        self.position += self.step_distance * direction

        big_position, small_position = self.positions
        reached_big = self.position <= big_position
        reached_small = self.position >= small_position
        done = reached_big or reached_small

        big_reward, small_reward, step_reward = self.rewards
        reward = (big_reward if reached_big else small_reward if reached_small else step_reward)

        return self.position, reward, done, None
