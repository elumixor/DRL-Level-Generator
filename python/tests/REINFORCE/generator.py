from torch.nn import Linear, Module, Softplus


class Generator(Module):
    def __init__(self):
        super().__init__()

        self.base = Linear(1, 4)
        self.head_mean = Linear(4, 1)
        self.head_std = Linear(4, 1)
        self.softplus = Softplus()

    def forward(self, difficulty):
        hidden = self.base(difficulty).relu()

        mean = self.head_mean(hidden)

        std = self.head_std(hidden)
        std = self.softplus(std) + 0.01

        return mean, std
