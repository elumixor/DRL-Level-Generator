import numpy as np
import torch
from torch.optim import Adam

from evaluators import DirectEvaluator
from evaluators.utils import calculate_diversity
from experiments import run_current
from generators import DirectGenerator


def main(context, max_angle, enemy_x_min, enemy_x_max, connector_length, enemy_radius, bob_radius,
         epochs, batch_size, lr, constrain, input_difficulty_sampling, diversity, diversity_weight,
         constrain_weight):
    generator = DirectGenerator(enemy_x_min, enemy_x_max, constrain)
    optim = Adam(generator.parameters(), lr=lr)
    evaluator = DirectEvaluator(connector_length, np.deg2rad(max_angle), enemy_radius, bob_radius)

    for epoch in range(epochs):
        if input_difficulty_sampling == "random":
            d_in = torch.rand(batch_size, 1)
        else:
            d_in = torch.linspace(0, 1, batch_size).unsqueeze(1)

        x, unconstrained_x = generator.forward(d_in)

        d_out = evaluator.evaluate(x)

        difficulty_difference = torch.linalg.norm(d_in - d_out, dim=-1).mean()

        if diversity:
            diversity = calculate_diversity(x.unsqueeze(0), d_in.unsqueeze(0))
        else:
            diversity = 0

        if not constrain:
            constrain_loss = 0
        else:
            constrain_loss = torch.linalg.norm(x - unconstrained_x, dim=-1).mean()

        # ↓ difficulty difference  ↑ diversity  ↓ constrain penalty
        loss = difficulty_difference - diversity_weight * diversity + constrain_weight * constrain_loss

        optim.zero_grad()
        loss.backward()
        optim.step()

        context.log({
            "difficulty difference": difficulty_difference,
            "diversity": diversity,
            "constrain penalty": constrain_loss
        })


if __name__ == '__main__':
    run_current(wandb=True)
