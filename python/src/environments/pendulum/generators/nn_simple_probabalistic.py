from typing import Optional

import numpy as np
import torch
import wandb
from scipy.stats import truncnorm
from torch.optim import Adam

from common import MLP
from .generator import PendulumGenerator


class SimpleProbabilisticNNGenerator(PendulumGenerator):
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

        # our nn will output the mean and the std of the truncated normal distribution
        self.nn = MLP(1, hidden[-1], hidden[:-1])
        self.head_mean = torch.nn.Linear(hidden[-1], 1)
        self.head_std = torch.nn.Linear(hidden[-1], 1)
        self.soft_relu = torch.nn.Softplus()

        self.parameters = list(self.nn.parameters()) + list(self.head_mean.parameters()) + list(
            self.head_std.parameters())
        self.optim = Adam(self.parameters, lr=lr)

    def forward(self, difficulties):
        hidden = self.nn(difficulties)
        mean = self.head_mean(hidden)
        std = self.head_std(hidden)
        std = self.soft_relu(std)

        return mean, std

    @torch.no_grad()
    def generate(self, difficulty: torch.Tensor, _: Optional[float] = None) -> torch.Tensor:
        mean, std = self.forward(difficulty)
        # std += 1e-5

        a, b = (self.min_x - mean) / std, (self.max_x - mean) / std
        samples = truncnorm.rvs(a, b)
        results = torch.from_numpy(samples).type(dtype=torch.float32)
        results = results * std + mean
        # print(results)
        # assert torch.all(results >= self.min_x) and torch.all(results <= self.max_x)
        return results

    def update(self, d_in: torch.Tensor, d_out: torch.Tensor, generated: torch.Tensor, diversity: torch.Tensor):
        # print("update")
        log_probabilities = torch.zeros_like(generated)
        means, stds = self.forward(d_in)

        for i, (mean, std, g) in enumerate(zip(means, stds, generated)):
            dist = torch.distributions.Normal(loc=mean, scale=std)

            # Truncate
            cdf_min = dist.cdf(self.min_x)
            cdf_max = dist.cdf(self.max_x)

            print(g)

            lp = dist.log_prob(g) - torch.log(cdf_max - cdf_min)
            print(dist.log_prob(g).exp())
            log_probabilities[i] = lp

        differences = torch.abs(d_in - d_out)
        # print(f"total differences: {differences.mean()}")

        loss_difficulty = (torch.abs(d_in - d_out) * log_probabilities).mean()
        loss_diversity = self.beta * diversity

        wandb.log({
            "mean difference": differences.mean().item(),
            "loss difficulty": loss_difficulty,
            "loss diversity": loss_diversity
        })

        self.optim.zero_grad()
        (loss_difficulty - loss_diversity).backward()

        total_grad = 0
        for p in self.parameters:
            total_grad += p.grad.data.sum()

        wandb.log({"total_grad": loss_diversity})

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
