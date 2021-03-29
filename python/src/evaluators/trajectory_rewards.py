import numpy as np
from numba import njit, typed, prange

from utilities import get_trajectory_reward


@njit(parallel=True)
def evaluate_levels(x, envs, actors, num_evaluations, max_trajectory_length):
    num_actors = len(actors)
    result = [0.0] * (len(x) * num_actors * num_evaluations)

    for i in prange(len(x)):
        level = x[i]
        for e in range(num_actors):
            actor = actors[e]
            for ev in prange(num_evaluations):
                index = i * num_actors * num_evaluations + e * num_evaluations + ev
                env = envs[index]
                env.set_level(level)
                r_trajectory = get_trajectory_reward(env, actor, max_trajectory_length)
                result[index] = r_trajectory

    return result


class TrajectoryRewardsEvaluator:
    def __init__(self, EnvClass, ActorClass, skills, skill_weights, num_envs, num_evaluations, max_trajectory_length,
                 env_args,
                 actor_args):
        self.actor_args = actor_args
        self.max_trajectory_length = max_trajectory_length
        self.num_evaluations = num_evaluations
        self.skill_weights = skill_weights
        self.envs = typed.List()
        for _ in range(num_envs):
            self.envs.append(EnvClass(0.0, *env_args))

        self.skills_number = skills.shape[0]
        self.actors = typed.List()
        for skill in skills.numpy().astype(np.float32):
            self.actors.append(ActorClass(skill, *actor_args))

        self.r_best = float("-inf")
        self.r_worst = float("inf")

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        """
        Evaluates the difficulty of levels by trajectory rewards.

        All of the trajectories are sampled. For each trajectory we record the total trajectory reward.
        We then find the r_best and r_worst are across all trajectories, evaluations.
        Then we calculate the difficulty of each trajectory as (r_best - r_trajectory) / (r_best - r_worst)
        Then we average all the difficulties of all evaluation of each sample.

        :param x: Levels to evaluate. Shape: [difficulties, samples, level]
        :return: Evaluated difficulties for each level. Shape: [difficulties, samples, 1]
        """
        num_difficulties = x.shape[0]
        num_samples = x.shape[1]

        r_trajectory = np.array(evaluate_levels(x.flatten(), self.envs, self.actors, self.num_evaluations,
                                                self.max_trajectory_length))
        r_trajectory = r_trajectory.reshape([num_difficulties, num_samples, self.skills_number, self.num_evaluations])

        # Update r_best and r_worst
        r_best = self.r_best = max(self.r_best, np.max(r_trajectory))
        r_worst = self.r_worst = min(self.r_worst, np.min(r_trajectory))

        # Calculate difficulties for each evaluation
        d_out = (r_best - r_trajectory) / (r_best - r_worst)

        # average the evaluations
        d_out = d_out.mean(axis=-1)

        # weight the skills
        d_out = (d_out * self.skill_weights).sum(axis=-1, keepdims=True)

        return d_out
