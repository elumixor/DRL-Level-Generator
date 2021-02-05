from typing import List

from torch.nn import Sequential, Linear, ReLU


def MLP(in_size: int, out_size: int, hidden_sizes: List[int]) -> Sequential:
    hidden_size = hidden_sizes[0] if len(hidden_sizes) > 0 else out_size

    layers = [
        Linear(in_size, hidden_size),
        ReLU(),
    ]

    for h in hidden_sizes:
        layers.append(Linear(hidden_size, h))
        layers.append(ReLU())
        hidden_size = h

    layers.append(Linear(hidden_size, out_size))

    return Sequential(*layers)
