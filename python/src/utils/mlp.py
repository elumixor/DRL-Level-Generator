from typing import Optional, List, Literal, Union

from torch import nn


class MLP(nn.Module):
    def __init__(self, in_size: int, out_size: int, hidden: Optional[List[int]] = None,
                 activation: Union[Literal["relu"], Literal["lrelu"]] = "relu", **kwargs):
        super().__init__()

        if hidden is None:
            hidden = []

        for h in hidden:
            if h <= 0:
                raise AttributeError(f"Hidden size should be greater than zero. Received: {hidden}")

        if not hidden:
            layers = [nn.Linear(in_size, out_size)]
        else:
            layers = [nn.Linear(in_size, hidden[0])]

            for i in range(len(hidden) - 1):
                layers.append(nn.Linear(hidden[i], hidden[i + 1]))

            layers.append(nn.Linear(hidden[-1], out_size))

        self.activation = nn.ReLU() if activation == "relu" else nn.LeakyReLU(kwargs.get("negative_slope", 1e-2))
        self.layers = nn.ModuleList(layers)

    def forward(self, x):
        # noinspection PyTypeChecker
        for layer in self.layers[:-1]:
            x = self.activation(layer(x))

        x = self.layers[-1](x)

        return x
