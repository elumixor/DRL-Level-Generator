from typing import Literal

from torch.nn import Module, Linear, Softplus, LeakyReLU


class ProbabilisticGenerator(Module):
    """
    Outputs the mean and std for the x position
    """

    def __init__(self, min_std: float, std_constrain: Literal["clamp", "softplus"] = "softplus"):
        super().__init__()
        self.l1 = Linear(1, 2)

        self.lrelu = LeakyReLU()

        self.mean = Linear(2, 1)
        self.std = Linear(2, 1)

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

    def forward(self, x):
        x = self.l1(x)
        x = self.lrelu(x)

        mean = self.mean(x)

        std = self.std(x)
        std = self.constrain(std)

        return mean, std
