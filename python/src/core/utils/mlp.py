from torch.nn import Sequential, Linear, ReLU, Module


def mlp(in_size: int, out_size: int, hidden_sizes=None) -> Module:
    if hidden_sizes is None:
        hidden_sizes = []

    if len(hidden_sizes) == 0:
        return Linear(in_size, out_size)

    hidden_size = hidden_sizes[0]

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
