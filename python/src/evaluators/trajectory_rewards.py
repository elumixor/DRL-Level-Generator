from multiprocessing import Pool

import torch

from utilities import get_trajectory_reward


def evaluate_levels(samples, skills, EnvClass, ActorClass, num_samples, skills_number, num_evaluations,
                    max_trajectory_length, env_args, actor_args):
    r_trajectory = torch.zeros([num_samples, skills_number, num_evaluations])
    for j in range(num_samples):
        level = samples[j]
        for s in range(skills_number):
            skill = skills[s]
            for e in range(num_evaluations):
                env = EnvClass(level, *env_args)
                actor = ActorClass(env, skill, *actor_args)

                r_trajectory[j][s][e] = get_trajectory_reward(env, actor, max_trajectory_length)

    return r_trajectory


class TrajectoryRewardsEvaluator:
    def __init__(self, EnvClass, ActorClass, skills, skill_weights, num_evaluations, max_trajectory_length, env_args,
                 actor_args):
        self.actor_args = actor_args
        self.env_args = env_args
        self.max_trajectory_length = max_trajectory_length
        self.num_evaluations = num_evaluations
        self.skill_weights = skill_weights
        self.skills = skills
        self.EnvClass = EnvClass
        self.ActorClass = ActorClass

        self.r_best = float("-inf")
        self.r_worst = float("inf")

    def evaluate(self, x):
        """
        Evaluates the difficulty of levels by trajectory rewards.

        All of the trajectories are sampled. For each trajectory we record the total trajectory reward.
        We then find the r_best and r_worst are across all trajectories, evaluations.
        Then we calculate the difficulty of each trajectory as (r_best - r_trajectory) / (r_best - r_worst)
        Then we average all the difficulties of all evaluation of each sample.

        :param x: Levels to evaluate. Shape: [difficulties, samples, level]
        :return: Evaluated difficulties for each level. Shape: [difficulties, samples, 1]
        """
        num_samples = x.shape[1]

        skills_number = self.skills.shape[0]

        with Pool() as pool:
            results = pool.starmap(evaluate_levels, [(sample, self.skills, self.EnvClass, self.ActorClass, num_samples,
                                                      skills_number, self.num_evaluations, self.max_trajectory_length,
                                                      self.env_args, self.actor_args) for sample in x])
        # [difficulties, samples, skills, evaluations]
        r_trajectory = torch.stack(results)

        # Update r_best and r_worst
        r_best = self.r_best = max(self.r_best, r_trajectory.max())
        r_worst = self.r_worst = min(self.r_worst, r_trajectory.min())

        # Calculate difficulties for each evaluation
        d_out = (r_best - r_trajectory) / (r_best - r_worst)

        # average the evaluations
        d_out = d_out.mean(dim=-1)

        # weight the skills
        d_out = (d_out * self.skill_weights).sum(dim=-1, keepdim=True)

        return d_out
