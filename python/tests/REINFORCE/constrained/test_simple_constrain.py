import torch
from torch.distributions import Normal
from torch.nn import Module, Linear, Softplus
from torch.optim import Adam


class G(Module):
    def __init__(self):
        super().__init__()
        self.hidden = Linear(1, 4)
        self.mean_head = Linear(4, 1)
        self.std_head = Linear(4, 1)
        self.softplus = Softplus()

    def forward(self, x):
        hidden = self.hidden(x)
        hidden = hidden.relu()

        mean = self.mean_head(hidden)
        std = self.std_head(hidden)
        std = self.softplus(std)

        return mean, std


generator = G()
optim = Adam(generator.parameters(), lr=0.01)

# Let's generate numbers between 0 and 2
min = 0
max = 2

for _ in range(1000):
    input = torch.rand([100, 1])

    mean, std = generator(input)
    dist = Normal(mean, std)

    with torch.no_grad():
        sample = dist.sample([100])

    clamped = sample.clamp(min, max)
    differences = (sample - clamped) ** 2

    print(f"{differences.mean().item():10.5f}")

    log_probs = dist.log_prob(sample)

    loss = (differences * log_probs).mean()

    optim.zero_grad()
    loss.backward()
    optim.step()
