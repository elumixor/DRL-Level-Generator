from typing import Optional, Union

import numpy as np
import torch
import torch.nn.functional as F
from torch.optim import Adam

from common import MLP
from common.remap import Remap
from .generator import PendulumGenerator
from ..state import PendulumState


class NNGenerator(PendulumGenerator):
    """
    Generates an enemy X position using NN
    """

    def __init__(self, hidden=None, lr=0.01, min_x=-0.5, max_x=0.5, beta=0.1,
                 bob_radius=0.15, max_angle=np.deg2rad(30), connector_length=0.5):
        if hidden is None:
            hidden = [8, 8]

        self.min_x = min_x
        self.max_x = max_x

        self.enemy_radius = 0.1
        self.enemy_y = 0.25

        self.bob_radius = bob_radius
        self.max_angle = max_angle
        self.connector_length = connector_length
        self.lr = lr
        self.beta = beta

        self.nn = MLP(1, 1, hidden)
        self.nn.add_module("remap", Remap(min_x, max_x))
        self.optim = Adam(self.nn.parameters(), lr=lr)

    def generate(self, difficulty: Union[float, torch.Tensor], _: Optional[float] = None) -> PendulumState:
        enemy_x = self.nn(difficulty)
        return enemy_x

    def update(self, d_in: torch.Tensor, d_out: torch.Tensor, diversity: torch.Tensor):
        loss_difficulty, loss_diversity = F.mse_loss(d_in, d_out), self.beta * diversity

        self.optim.zero_grad()
        (loss_difficulty - loss_diversity).backward()
        self.optim.step()

        return loss_difficulty.item(), loss_diversity.item()

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
            "lr": self.lr,
            "beta": self.beta
        }
