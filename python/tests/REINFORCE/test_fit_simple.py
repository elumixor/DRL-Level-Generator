import torch
from torch.nn import Module, Linear, Softplus
from torch.optim import Adam

from test_common import BaseTest


class Generator(Module):
    def __init__(self):
        super().__init__()

        self.base = Linear(1, 4)
        self.head_mean = Linear(4, 1)
        self.head_std = Linear(4, 1)
        self.softplus = Softplus()

    def forward(self, difficulty):
        hidden = self.base(difficulty)
        mean = self.head_mean(hidden)

        std = self.head_std(hidden)
        std = self.softplus(std)

        return mean, std


class Test(BaseTest):
    @BaseTest.confidence(45, 50)
    def test_fitting_constant(self):
        """
        Tries to fit a constant distance to a target
        :return:
        """
        # Called to reset smooth values
        self.reset_experiment()

        target = torch.rand([1])
        x = torch.tensor([0.5])
        num_samples = 100

        generator = Generator()
        optim = Adam(generator.parameters(), lr=0.01)

        for epoch in range(100):
            # Collect data
            with torch.no_grad():
                mean, std = generator(x)

                sample = torch.distributions.Normal(mean, std).sample([num_samples])
                difference = (sample - target) ** 2

            # Train
            mean, std = generator(x)

            distribution = torch.distributions.Normal(mean, std)

            log_prob = distribution.log_prob(sample)
            weighted = difference * log_prob

            # We want to DECREASE the probabilities of the samples with HIGH w.eights
            loss = weighted.mean()

            optim.zero_grad()
            loss.backward()
            optim.step()

            self.assert_decreases("difference", difference.mean(), window_size=50)

            # Validate
            with torch.no_grad():
                mean, std = generator(x)
                difference = (mean - target) ** 2
                validation = difference.item()

            self.assert_decreases("loss", validation, window_size=50, threshold=0.001)
