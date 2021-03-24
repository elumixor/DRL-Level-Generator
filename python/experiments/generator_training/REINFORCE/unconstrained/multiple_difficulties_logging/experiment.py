import torch
import wandb
from torch.distributions import Normal
from torch.optim import Adam

from experiments import run_current
from experiments.commands import delete_runs
from experiments.runner import get_runs
from generators.probabilistic import ProbabilisticGenerator
from test_utils import ConvergenceChecker
# Generate actual levels, place the enemy and use heuristic evaluator
from utilities.recorder import Recorder


def main(context, epochs, sample_size, lr, min_std, std_constrain, convergence, target, trial):
    generator = ProbabilisticGenerator(min_std, std_constrain)
    optim = Adam(generator.parameters(), lr=lr)

    checker = ConvergenceChecker(convergence.steps, convergence.threshold, record_all=False)

    # Cover the input difficulties domain
    d_in = torch.linspace(0, 1, 10).unsqueeze(1)

    recorder = Recorder()

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

        # Compute basic loss of the clamped samples
        # d_out will just be the distance from the target
        # this is simply how we chose it to be for this case
        d_out = (x - target).abs()

        # Difference in the difficulties we will minimize
        # d_in shape [batch_size, 1] -> [batch_size, 1, 1] -> [batch_size, sample_size, 1]
        difference = (d_out - d_in.unsqueeze(1)).abs()

        # Weight everything together
        # - minimize the difference in d_in and d_out
        # - minimize the difference between x and x_constrained
        loss = (difference * log_prob).mean()

        # Total weighted loss
        optim.zero_grad()
        loss.backward()
        optim.step()

        # Validate using the clamped mean`
        with torch.no_grad():
            d_out = (mean - target).abs()  # [batch_size, 1]
            validation_difference = (d_out - d_in).abs().mean()

        # Log stuff
        recorder.record(**{
            "difference": difference.mean(),
            "validation difference": validation_difference,
            "mean": mean,
            "std": std,
            **{f"{d_in[i].item():.4f}": diff for i, diff in enumerate(difference.mean(dim=1).flatten().tolist())}
        })

        # Early stop if converged
        if checker.step(validation_difference):
            break

    entries = recorder.entries

    run = wandb.init(project="Level Generator",
                     name="Multiple difficulties logging",
                     config={
                         "name": "multiple_difficulties_logging",
                         "sample_size": sample_size,
                         "lr": lr,
                         "min_std": min_std,
                         "std_constrain": std_constrain,
                         "convergence": convergence,
                         "target": target,
                     })
    for key, values in entries.items():
        entries[key] = [(key, item) for item in values]

    for entry in zip(*entries.values()):
        # entry is an array of pairs (name, value)
        run.log({
            **{key: item for key, item in entry}
        })

    run.finish()


if __name__ == '__main__':
    runs = get_runs("elumixor", "Level Generator", "multiple_difficulties_logging")
    delete_runs(runs)
    run_current(silent=True, args={
        "trials": 1
    })
