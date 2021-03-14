import torch
from torch.nn import Module, Linear, Softplus
from torch.optim import Adam

import wandb


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


if __name__ == '__main__':
    for _ in range(10):
        target = torch.rand([1])
        num_samples = 100
        batch_size = 100

        generator = Generator()
        lr = 0.01
        optim = Adam(generator.parameters(), lr=lr)
        # scheduler = LambdaLR(optim, lambda epoch: 0.999 ** epoch)

        run = wandb.init(project="Heuristic", name="Dynamic fit", config={
            "lr": lr,
            # "scheduler": "lambda",
            "factor": 0.999
        })

        for epoch in range(2000):
            # Batch of inputs
            x = torch.rand([batch_size, 1])

            # Collect data
            with torch.no_grad():
                mean, std = generator(x)

                sample = torch.distributions.Normal(mean, std).sample([num_samples])
                distance = (sample - target) ** 2

                difference = (distance - x) ** 2

            # Train
            mean, std = generator(x)

            distribution = torch.distributions.Normal(mean, std)

            log_prob = distribution.log_prob(sample)
            weighted = difference * log_prob

            # We want to DECREASE the probabilities of the samples with HIGH differences
            loss = weighted.mean()

            optim.zero_grad()
            loss.backward()
            optim.step()

            wandb.log({"difference": difference.mean()})

            # Validate
            with torch.no_grad():
                x = torch.rand([batch_size, 1])
                mean, _ = generator(x)
                distance = (mean - target) ** 2
                difference = (distance - x) ** 2
                validation = difference.mean().item()

                wandb.log({"validation loss": validation})

            # scheduler.step()
            # wandb.log({"lr": scheduler.get_last_lr()[0]})

        run.finish()
