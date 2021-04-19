from typing import Union

import torch.nn as nn


class Remap(nn.Module):
    def __init__(self, min: Union[int, float], max: Union[int, float]):
        super().__init__()

        self.min = min
        self.diff = max - min

    def forward(self, x):
        return x.sigmoid() * self.diff + self.min
