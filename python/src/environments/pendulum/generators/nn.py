from typing import Optional

import numpy as np
import torch
from torch.optim import Adam

from common import MLP
from common.remap import Remap
from .generator import PendulumGenerator
from ..state import PendulumState


class NNGenerator(PendulumGenerator):
    def __init__(self, hidden=None, lr=0.01, speed=0.01, fast_speed=0.1, min_x=-0.5, max_x=0.5,
                 min_y=-0.25, max_y=0.75, bob_radius=0.15, max_angle=np.deg2rad(30), angle=np.deg2rad(30),
                 angular_speed=np.deg2rad(5), vertical_speed=0.02, connector_length=0.5):
        if hidden is None:
            hidden = [8, 8]

        self.speed = speed
        self.fast_speed = fast_speed
        self.min_x = min_x
        self.max_x = max_x

        self.min_y = min_y
        self.max_y = max_y

        self.enemy_radius = 0.1
        self.enemy_y = 0.25

        self.bob_radius = bob_radius
        self.max_angle = max_angle
        self.connector_length = connector_length
        self.vertical_speed = vertical_speed
        self.angle = angle
        self.angular_speed = angular_speed
        self.lr = lr

        self.nn = MLP(1, 1, hidden)
        self.nn.add_module("remap", Remap(min_x, max_x))
        self.optim = Adam(self.nn.parameters(), lr=lr)

    def generate(self, difficulty: float, _: Optional[float] = None) -> PendulumState:
        position = 0
        enemy_x = self.nn(torch.tensor([difficulty]))

        return PendulumState(self.bob_radius, self.max_angle, self.connector_length, self.vertical_speed,
                             enemy_x, self.enemy_y, self.enemy_radius,
                             self.angle, position, self.angular_speed)

    def update(self, loss: torch.Tensor):
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

    @property
    def config(self):
        return {
            "Enemy x (min)": self.min_x,
            "Enemy x (max)": self.max_x,
            "Enemy y": self.enemy_y,
            "Enemy radius": self.enemy_radius,
            "Bob radius": self.bob_radius,
            "Max angle": self.max_angle,
            "Connector length": self.connector_length,
            "Vertical speed": self.vertical_speed,
            "angle": self.angle,
            "Angular speed": self.angular_speed,
            "lr": self.lr,
        }
