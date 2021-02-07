from typing import Optional

import numpy as np

from .agents import Agent
from .environments import Environment, RenderableEnvironment
from .trajectory import Trajectory
from .utils import discounted_rewards, EpsilonDecay


def train(env: Environment, agent: Agent, epochs=100, num_trajectories=5, render_frequency: Optional[int] = None,
          cutoff_at=200, validation_frequency: Optional[int] = None, num_validation_trajectories=15,
          save_path: Optional[str] = None):
    best_mean_total_reward = -np.inf
    p = 0.0
    for epoch in range(epochs):
        agent.train()
        trajectories = [Trajectory.sample(env, agent, cutoff_at=cutoff_at) for _ in range(num_trajectories)]
        agent.update(trajectories)

        if render_frequency is not None and epoch != 0 and epoch % render_frequency == 0:
            agent.eval()
            Trajectory.sample(env, agent, cutoff_at=cutoff_at).render(env)

        if validation_frequency is not None and epoch != 0 and epoch % validation_frequency == 0:
            agent.eval()
            validation_trajectories = [Trajectory.sample(env, agent, cutoff_at=cutoff_at) for _ in
                                       range(num_validation_trajectories)]
            mean_total_reward = np.mean([t.total_reward for t in validation_trajectories])
            print(f"Validation mean total reward: {mean_total_reward}")

            if save_path is not None and mean_total_reward > best_mean_total_reward:
                best_mean_total_reward = mean_total_reward
                agent.save(save_path)

        next_p = epoch / (epochs - 1)
        if next_p - p > 0.01:
            p += 0.01
            agent.print_progress()
            agent.plot_progress()


def evaluate(env: Environment, agent: Agent, num_trajectories=5, cutoff_at=np.inf):
    agent.eval()
    for _ in range(num_trajectories):
        t = Trajectory.sample(env, agent, cutoff_at=cutoff_at)
        t.render(env)
        print(f"Total reward: {t.total_reward}")
