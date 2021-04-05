import signal

import numpy as np
import torch
from torch.distributions import Normal
from torch.optim import Adam

from evaluators import DirectEvaluator
from experiments import run_current
from generators import ProbabilisticSeededGenerator
from test_utils import ConvergenceChecker


# Generate actual levels, place the enemy and use heuristic evaluator

def main(context, enemy_x_min, enemy_x_max, epochs, batch_size, sample_size, lr, constrain_weight, min_std,
         std_constrain, convergence, max_angle, connector_length, enemy_radius, bob_radius, seed, trial,
         diversity_weight):
    seed_total, seed_sample = seed["total"], seed["sample"]

    # todo: can be class-jitted
    seed_base = np.linspace(0, 1, seed_total, dtype=np.float32)

    # If we run in parallel, sometimes cuda will not be available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # device = "cpu"

    generator = ProbabilisticSeededGenerator(min_std, std_constrain).to(device)
    optim = Adam(generator.parameters(), lr=lr)
    evaluator = DirectEvaluator(connector_length, np.deg2rad(max_angle).item(), enemy_radius, bob_radius)

    checker = ConvergenceChecker(convergence.steps, convergence.threshold, record_all=False)

    # Cover the input difficulties domain
    d_in = torch.linspace(0, 1, batch_size, device=device)

    interrupt = False

    def signal_handler(sig, frame):
        global interrupt
        interrupt = True

    signal.signal(signal.SIGINT, signal_handler)

    # Batch of inputs
    for _ in range(epochs):
        if interrupt:
            break

        seeds = torch.from_numpy(np.random.choice(seed_base, seed_sample, replace=False)).to(device)

        # Generate mean and std, create a distribution
        mean, std = generator(d_in, seeds)
        distribution = Normal(mean, std)

        # Sample from the distribution and the log probabilities
        x = distribution.sample([sample_size])
        log_prob = distribution.log_prob(x)

        # Transpose to [difficulty, epsilon, sample, 1]
        x = x.permute(1, 2, 0, 3)
        log_prob = log_prob.permute(1, 2, 0, 3)

        flattened = x.reshape([batch_size, seed_sample * sample_size, -1])
        flattened_differences = torch.linalg.norm(flattened.unsqueeze(1) - flattened.unsqueeze(2), dim=-1)

        seeds_difference = (seeds.unsqueeze(0) - seeds.unsqueeze(1)).abs()

        # Repeat seeds difference for the samples, generated with the same epsilon
        # e.g.
        #                 [[1, 1, 0, 0]
        # [[1, 0]   ->     [1, 1, 0, 0]
        #  [2, 3]          [2, 2, 3, 3]
        #                  [2, 2, 3, 3]]
        seeds_difference = torch.repeat_interleave(seeds_difference, sample_size, dim=0)
        seeds_difference = torch.repeat_interleave(seeds_difference, sample_size, dim=1)

        diversity = seeds_difference * flattened_differences
        sample_diversity = diversity.mean(dim=-1)

        sample_diversity = sample_diversity.reshape([batch_size, seed_sample, sample_size, 1])

        # Constrain the samples to a valid range
        x_constrained = x.clamp(enemy_x_min, enemy_x_max)

        # Compute basic loss of the clamped samples
        # d_out will just be the distance from the target
        # this is simply how we chose it to be for this case
        d_out = evaluator.evaluate(x_constrained)

        # Difference in the difficulties we will minimize
        # d_in shape [batch_size, 1] -> [batch_size, 1, 1] -> [batch_size, sample_size, 1]
        difference = (d_out - d_in.reshape(-1, 1, 1, 1)).abs()

        # Compute the clamp penalty
        clamp_penalty = torch.linalg.norm(x_constrained - x, dim=-1, keepdim=True)

        # Weight everything together
        # - minimize the difference in d_in and d_out
        # - minimize the difference between x and x_constrained
        # + maximize the diversity
        loss = ((difference + constrain_weight * clamp_penalty - diversity_weight * sample_diversity) * log_prob).mean()

        # Total weighted loss
        gradient = 0
        optim.zero_grad()
        loss.backward()

        with torch.no_grad():
            for p in generator.parameters():
                gradient += p.grad.data.abs().sum()

        optim.step()

        # Validate using the clamped mean
        with torch.no_grad():
            clamped_mean = mean.clamp(enemy_x_min, enemy_x_max)  # [batch_size, 1]
            d_out = evaluator.evaluate(clamped_mean)  # [batch_size, 1]
            validation_difference = (d_out - d_in.reshape(-1, 1, 1)).abs().mean()

        # Log stuff
        context.log({
            "difference": difference.mean(),
            "clamp penalty": clamp_penalty.mean(),
            "validation difference": validation_difference,
            "diversity": sample_diversity.mean(),
            "gradient": gradient,
            "mean of the std": std.mean(),
        })

        # Early stop if converged
        if checker.step(validation_difference):
            break

    plot_results(generator)


@torch.no_grad()
def plot_results(generator):
    generator.cpu()

    d_in = torch.linspace(0, 1, 100)
    epsilon = torch.linspace(0, 1, 100)

    mean, _ = generator.forward(d_in, epsilon)

    import matplotlib.pyplot as plt
    from matplotlib import cm

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.

    d_in = np.linspace(0, 1, 100)
    epsilon = np.linspace(0, 1, 100)
    d_in, epsilon = np.meshgrid(d_in, epsilon)

    # Plot the surface.
    surf = ax.plot_surface(d_in, epsilon, mean.squeeze().numpy(), cmap=cm.coolwarm,
                           linewidth=0, antialiased=True)

    ax.set_xlabel('seed')
    ax.set_ylabel('d_in')
    ax.set_zlabel('x')

    fig.tight_layout()

    plt.show()


if __name__ == '__main__':
    run_current(wandb=True, parallel=False)
