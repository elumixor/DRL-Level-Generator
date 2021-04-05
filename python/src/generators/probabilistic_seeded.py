from typing import Literal

import torch
from torch.nn import Module, Linear, Softplus


class ProbabilisticSeededGenerator(Module):
    """
    Outputs the mean and std for the x position
    """

    def __init__(self, min_std: float, std_constrain: Literal["clamp", "softplus"] = "softplus"):
        super().__init__()
        self.l1 = Linear(2, 8)  # l1 has an input size 2 instead of 1
        self.l2 = Linear(8, 8)  # l1 has an input size 2 instead of 1
        # self.l1 = Identity()

        self.mean = Linear(8, 1)
        self.std = Linear(8, 1)

        if std_constrain == "softplus":
            softplus = Softplus()

            def constrain(x):
                return softplus(x) + min_std

            self.constrain = constrain

        elif std_constrain == "clamp":
            def constrain(x):
                return x.clamp(min=min_std)

            self.constrain = constrain

        else:
            raise ValueError(f"Std constrain should be either \"clamp\" or \"softplus\". Received \"{std_constrain}\"")

    def forward(self, d_in, seed):
        x = torch.cartesian_prod(d_in, seed)  # aggregate the difficulty and seed
        x = x.reshape(d_in.shape[0], seed.shape[0], 2)

        x = self.l1(x).relu()
        x = self.l2(x).relu()

        mean = self.mean(x)

        std = self.std(x)
        std = self.constrain(std)

        return mean, std
