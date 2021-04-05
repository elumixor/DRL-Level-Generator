import numpy as np
import torch

from actor import Actor
from environment import Environment
from evaluators import TrajectoryRewardsEvaluator
from experiments import run_current
from generators import GeneratorWrapper
from generators.probabilistic import ProbabilisticGenerator
from utilities import weight_skills


def main(context, min_std, std_constrain, lr, skills, epochs, d_in_size, enemy_x_min, enemy_x_max, sample_size,
         constrain_weight, num_evaluations, max_trajectory_length, skill_weighting, action_distance,
         bob_radius, max_angle, connector_length, vertical_speed,
         enemy_y, enemy_radius, current_angle, position, angular_speed):
    generator = GeneratorWrapper(ProbabilisticGenerator(min_std, std_constrain),
                                 lr, sample_size, enemy_x_min, enemy_x_max)

    env_args = [bob_radius, np.deg2rad(max_angle), connector_length, vertical_speed, enemy_y, enemy_radius,
                np.deg2rad(current_angle), position, np.deg2rad(angular_speed)]

    actor_args = [action_distance]

    skill_weights = weight_skills(torch.tensor(skills), skill_weighting.mean, skill_weighting.std,
                                  skill_weighting.skew)

    num_envs = d_in_size * sample_size * len(skills) * num_evaluations
    evaluator = TrajectoryRewardsEvaluator(Environment, Actor, torch.tensor(skills), skill_weights, num_envs,
                                           num_evaluations, max_trajectory_length, env_args, actor_args)

    # generate input difficulties (systematically)
    d_in = torch.linspace(0, 1, d_in_size).unsqueeze(1)
    for epoch in range(epochs):
        print(epoch)

        # Generate the levels, get their log probabilities and constrain loss
        level, log_prob, constrain_loss = generator.generate(d_in)

        # Evaluate the difficulty of the generated levels
        d_out = torch.from_numpy(evaluator.evaluate(level.numpy())).type(torch.float32)

        # Compute the difference with the input difficulty
        difference = (d_out - d_in.unsqueeze(1)).abs()

        # Minimize the difference and constrain loss
        loss = ((difference + constrain_weight * constrain_loss) * log_prob).mean()

        gradient = generator.fit(loss)

        context.log({
            "difference": difference.mean(),
            "constrain loss": constrain_loss.mean(),
            "gradient": gradient,
        })


if __name__ == '__main__':
    run_current(wandb=True, parallel=False)
