from torch.nn import Module, Linear, Softplus


class Simple(Module):
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
        std = self.softplus(std)

        return mean, std
