from typing import Union

import torch
import torch.nn as nn


class Clamp(nn.Module):
    def __init__(self, min: Union[int, float], max: Union[int, float]):
        super().__init__()

        self.min = min
        self.max = max

    def forward(self, x: torch.Tensor):
        return x.clamp(self.min, self.max)
