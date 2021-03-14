import torch
from torch.distributions import Normal
from torch.optim import Adam

import wandb
from common import read_yaml, StepCounter
from generator import Simple

if __name__ == '__main__':
    config = read_yaml("config")

    step_counter = StepCounter(config.trials * config.epochs, frequency=100, name="Epoch")

    for _ in range(config.trials):
        target = torch.rand([1])

        generator = Simple()
        optim = Adam(generator.parameters(), lr=config.lr)

        run = wandb.init(project="Heuristic", name="Constrained dynamic fit", config=config)

        # Batch of inputs
        for epoch in range(config.epochs):
            x = torch.rand([config.batch_size, 1])

            mean, std = generator(x)
            distribution = Normal(mean, std)

            # Collect data
            with torch.no_grad():
                unclamped = distribution.sample([config.num_samples])

            # Clamp the samples
            clamped = unclamped.clamp(config.min, config.max)

            # Compute basic loss of the clamped samples
            distance = (clamped - target) ** 2
            difference = (distance - x) ** 2

            # Compute the clamp penalty
            clamp_penalty = (clamped - unclamped) ** 2

            # Weight everything together
            weight = difference + config.penalty_weight * clamp_penalty
            loss = weight * distribution.log_prob(unclamped)

            # Total weighted loss
            optim.zero_grad()
            loss.mean().backward()
            optim.step()

            # Validate using the clamped mean
            with torch.no_grad():
                clamped_mean = mean.clamp(config.min, config.max)
                validation_penalty = (clamped_mean - mean) ** 2
                distance = (clamped_mean - target) ** 2
                validation_difference = (distance - x) ** 2

            # Log stuff
            wandb.log({
                "difference": difference.mean(),
                "clamp penalty": clamp_penalty.mean(),
                "validation difference": validation_difference.mean(),
                "validation penalty": validation_penalty.mean(),
                "epoch": epoch
            })

            step_counter.step()

        run.finish()
