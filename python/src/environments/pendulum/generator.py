import random
from enum import Enum
from typing import Optional

import numpy as np
import torch

from core.utils import MLP
from environments.pendulum.transition import parameters_size


class I(int, Enum):
    bob_radius = 0
    max_angle = 1
    connector_length = 2
    vertical_speed = 3
    enemies_count = 4

    enemy_start = 5

    enemy_radius = 0
    enemy_x = 1
    enemy_y = 2
    enemy_size = 3

    angle = 0
    position = 1
    angular_speed = 2
    enemies_count_dynamic = 3


class Constraints:
    bob_radius = torch.tensor([0.1, 1])
    max_angle = np.pi * torch.tensor([0.1, 0.5])
    connector_length = torch.tensor([0.1, 1.5])
    vertical_speed = torch.tensor([0.1, 2])
    enemies_count = torch.tensor([1, 1])

    enemy_radius = torch.tensor([0.1, 1])
    enemy_x = torch.tensor([-1, 1])
    enemy_y = torch.tensor([0.5, 0.5])

    position = torch.tensor([0, 0])
    angular_speed = torch.tensor([-1, 1])


class Generator:
    def __init__(self, hidden=None):
        if hidden is None:
            hidden = [8, 8]

        self.network = MLP(2, parameters_size, hidden)

    def generate(self, difficulty: Optional[float] = None, random_seed: Optional[float] = None) -> torch.Tensor:
        if difficulty is None:
            difficulty = random.random()

        if random_seed is None:
            random_seed = random.random()

        output = self.network(torch.tensor([difficulty, random_seed]))

        output[I.bob_radius] = torch.clamp(output[I.bob_radius], *Constraints.bob_radius)
        output[I.max_angle] = torch.clamp(output[I.max_angle], *Constraints.max_angle)
        output[I.connector_length] = torch.clamp(output[I.connector_length], *Constraints.connector_length)
        output[I.vertical_speed] = torch.clamp(output[I.vertical_speed], *Constraints.vertical_speed)
        output[I.enemies_count] = torch.clamp(output[I.enemies_count], *Constraints.enemies_count)

        for i in range(int(output[I.enemies_count].item())):
            enemy_radius = output[I.enemy_start + I.enemy_radius + I.enemy_size * i]
            enemy_radius = torch.clamp(enemy_radius, *Constraints.enemy_radius)
            output[I.enemy_start + I.enemy_radius + I.enemy_size * i] = enemy_radius

            enemy_x = output[I.enemy_start + I.enemy_x + I.enemy_size * i]
            enemy_x = torch.clamp(enemy_x, *Constraints.enemy_x)
            output[I.enemy_start + I.enemy_x + I.enemy_size * i] = enemy_x

            enemy_y = output[I.enemy_start + I.enemy_y + I.enemy_size * i]
            enemy_y = torch.clamp(enemy_y, *Constraints.enemy_y)
            output[I.enemy_start + I.enemy_y + I.enemy_size * i] = enemy_y

        offset = I.enemy_start + I.enemy_size * output[I.enemies_count].int()

        output[offset + I.angle] = torch.clamp(output[offset + I.angle], -output[I.max_angle].item(),
                                               output[I.max_angle].item())
        output[offset + I.position] = torch.clamp(output[offset + I.angle], *Constraints.position)
        output[offset + I.angular_speed] = torch.clamp(output[offset + I.angular_speed], *Constraints.angular_speed)
        output[offset + I.enemies_count_dynamic] = output[I.enemies_count]

        return output

    def __call__(self, difficulty: Optional[float] = None, random_seed: Optional[float] = None) -> torch.Tensor:
        return self.generate(difficulty, random_seed)
