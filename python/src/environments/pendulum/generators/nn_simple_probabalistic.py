from typing import Optional, Tuple

import numpy as np
import torch
import wandb
from torch.distributions import Normal
from torch.nn import Linear, Softplus, Module, LeakyReLU
from torch.optim import Adam

from .generator import PendulumGenerator


class SimpleProbabilisticNNGenerator(PendulumGenerator):
    """
    Generates an enemy X position using NN
    """

    def __init__(self, lr=0.01, min_x=-0.5, max_x=0.5, bob_radius=0.15, max_angle=np.deg2rad(30),
                 beta=0.1,
                 connector_length=0.5):
        self.min_x = min_x
        self.max_x = max_x

        self.enemy_radius = 0.1
        self.enemy_y = 0.25

        self.bob_radius = bob_radius
        self.max_angle = max_angle
        self.connector_length = connector_length
        self.lr = lr
        self.beta = beta

        # our nn will output the mean and the std of the truncated normal distribution
        class NN(Module):
            def __init__(self):
                super().__init__()

                self.hidden = Linear(1, 4)
                self.relu = LeakyReLU()
                self.head_mean = Linear(4, 1)
                self.head_std = Linear(4, 1)
                self.softplus = Softplus()

            def forward(self, x):
                x = self.hidden(x)
                x = self.relu(x)

                mean = self.head_mean(x)

                std = self.head_std(x)
                std = self.softplus(std)

                return mean, std

        self.nn = NN()
        self.optim = Adam(self.nn.parameters(), lr=lr)

    @torch.no_grad()
    def generate(self, difficulty: torch.Tensor, _: Optional[float] = None, num_samples=100) -> Tuple[torch.Tensor,
                                                                                                      torch.Tensor]:
        mean, std = self.nn(difficulty)
        dist = Normal(mean, std)
        x = dist.sample([num_samples])
        x_clamped = x.clamp(self.min_x, self.max_x)
        return x, x_clamped

    def update(self, d_in: torch.Tensor, d_out: torch.Tensor, x: torch.Tensor):
        mean, std = self.nn(d_in)
        dist = Normal(mean, std)
        log_probabilities = dist.log_prob(x)

        difficulty_difference = (d_out - d_in) ** 2

        # We compute the euclidean distance between each two generated levels
        # This is done for the batch of shape [d_in_size * num_samples * level_size]
        diversity = (x.unsqueeze(-2) - x.unsqueeze(-3)).abs().sum(dim=-1)
        diversity_weight = (d_out.unsqueeze(-2) - d_out.unsqueeze(-3)).abs().squeeze()
        weighted_diversity = diversity * diversity_weight

        # Now we have a symmetric matrix of weighted differences
        # We will average them for each sample over all other samples
        weighted_diversity = weighted_diversity.mean(dim=-1, keepdim=True)

        # print(weighted_diversity.shape)
        # print(difficulty_difference.shape)

        wandb.log({
            "difficulty difference": difficulty_difference.mean(),
            "diversity": weighted_diversity.mean()
        })

        loss = ((difficulty_difference - self.beta * weighted_diversity) * log_probabilities).mean()

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
            "lr": self.lr,
            "beta": self.beta
        }
