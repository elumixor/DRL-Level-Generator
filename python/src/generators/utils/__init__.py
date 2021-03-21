from typing import Literal

import torch


def get_input_difficulties(batch_size: int, input_difficulty_sampling: Literal["random", "systematic"]):
    if input_difficulty_sampling == "random":
        return torch.rand(batch_size, 1)
    elif input_difficulty_sampling == "systematic":
        return torch.linspace(0, 1, batch_size).unsqueeze(1)
