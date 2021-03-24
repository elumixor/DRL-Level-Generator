import torch
from torch.distributions import Normal
from torch.optim import Adam

from experiments import run_current
from generators.probabilistic import ProbabilisticGenerator
from test_utils import ConvergenceChecker


# Generate actual levels, place the enemy and use heuristic evaluator

def main(context, enemy_x_min, enemy_x_max, epochs, batch_size, sample_size, lr, constrain_weight, min_std,
         std_constrain, convergence, trial, target):
    print(f"{trial=}")

    generator = ProbabilisticGenerator(min_std, std_constrain)
    optim = Adam(generator.parameters(), lr=lr)

    checker = ConvergenceChecker(convergence.steps, convergence.threshold, record_all=False)

    # Cover the input difficulties domain
    d_in = torch.linspace(0, 1, batch_size).unsqueeze(1)

    # Batch of inputs
    for _ in range(epochs):
        # Generate mean and std, create a distribution
        mean, std = generator(d_in)
        distribution = Normal(mean, std)

        # Sample from the distribution and the log probabilities
        x = distribution.sample([sample_size])
        log_prob = distribution.log_prob(x)

        # Transpose to [batch_size, sample_size, 1]
        x = x.transpose(0, 1)
        log_prob = log_prob.transpose(0, 1)

        # Constrain the samples to a valid range
        x_constrained = x.clamp(enemy_x_min, enemy_x_max)

        # Compute basic loss of the clamped samples
        # d_out will just be the distance from the target
        # this is simply how we chose it to be for this case
        d_out = (x_constrained - target).abs()

        # Difference in the difficulties we will minimize
        # d_in shape [batch_size, 1] -> [batch_size, 1, 1] -> [batch_size, sample_size, 1]
        difference = (d_out - d_in.unsqueeze(1)).abs()

        # Compute the clamp penalty
        clamp_penalty = (x_constrained - x).abs()

        # Weight everything together
        # - minimize the difference in d_in and d_out
        # - minimize the difference between x and x_constrained
        loss = ((difference + constrain_weight * clamp_penalty) * log_prob).mean()

        # Total weighted loss
        optim.zero_grad()
        loss.backward()
        optim.step()

        # Validate using the clamped mean
        with torch.no_grad():
            clamped_mean = mean.clamp(enemy_x_min, enemy_x_max)  # [batch_size, 1]
            d_out = (clamped_mean - target).abs()  # [batch_size, 1]
            validation_difference = (d_out - d_in).abs().mean()

        # Log stuff
        context.log({
            "difference": difference.mean(),
            "clamp penalty": clamp_penalty.mean(),
            "validation difference": validation_difference,
            "mean of the std": std.mean(),
        })

        # Early stop if converged
        if checker.step(validation_difference):
            return


if __name__ == '__main__':
    run_current(wandb=True)
