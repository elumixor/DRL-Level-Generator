import torch

from .utils import MLP


class Generator:
    def __init__(self, output_size: int, hidden=None):
        if hidden is None:
            hidden = [8, 8]

        self.network = MLP(2, output_size, hidden)

    def generate(self, difficulty: float, random_seed: float = 0) -> torch.Tensor:
        return self.network(torch.tensor([difficulty, random_seed]))
