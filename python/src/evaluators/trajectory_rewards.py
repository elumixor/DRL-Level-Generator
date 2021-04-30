import numpy as np
import torch
from numba import prange, njit, typed
from numba.experimental import jitclass

from .utils import get_trajectory_reward


@njit(parallel=True)
def evaluate_levels(states, env, actors, num_evaluations, max_trajectory_length):
    result = np.zeros((states.shape[0], states.shape[1], (len(actors)), num_evaluations), dtype=np.float32)

    for i in prange(len(states)):
        samples = states[i]
        for s in prange(len(samples)):
            state = samples[s]
            for j in prange(len(actors)):
                actor = actors[j]
                for ev in prange(num_evaluations):
                    result[i][s][j][ev] = get_trajectory_reward(env, actor, state, max_trajectory_length)

    return result


class TrajectoryRewardsEvaluator:
    def __init__(self, env, actors, actors_weights, num_evaluations, max_trajectory_length):
        assert len(actors) == len(actors_weights)

        self.env = env
        self.actors = typed.List(actors)
        self.actors_weights = actors_weights

        self.max_trajectory_length = max_trajectory_length
        self.num_evaluations = num_evaluations

        self.r_best = float("-inf")
        self.r_worst = float("inf")

    def evaluate(self, states: np.ndarray) -> np.ndarray:
        """
        Evaluates the difficulty of levels by trajectory rewards.

        All of the trajectories are sampled. For each trajectory we record the total trajectory reward.
        We then find the r_best and r_worst are across all trajectories, evaluations.
        Then we calculate the difficulty of each trajectory as (r_best - r_trajectory) / (r_best - r_worst)
        Then we average all the difficulties of all evaluation of each sample.

        :param states: Levels to evaluate. Shape: [difficulties, samples, level]
        :return: Evaluated difficulties for each level. Shape: [difficulties, samples, 1]
        """
        r_trajectory = evaluate_levels(states, self.env, self.actors, self.num_evaluations, self.max_trajectory_length)

        # Update r_best and r_worst
        r_best = self.r_best = max(self.r_best, np.max(r_trajectory))
        r_worst = self.r_worst = min(self.r_worst, np.min(r_trajectory))

        # Calculate difficulties for each evaluation
        d_out = (r_best - r_trajectory) / (r_best - r_worst)

        # average the evaluations
        d_out = d_out.mean(axis=-1)

        # weight the skills
        d_out = (d_out * self.actors_weights).sum(axis=-1, keepdims=True)

        return d_out
