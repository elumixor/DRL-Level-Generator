from typing import Optional

import numpy as np

from common import log
from .agents import Agent
from .environments import Environment, RenderableEnvironment
from .trajectory import Trajectory


def train(env: Environment, agent: Agent, epochs=100, num_trajectories=5, render_frequency: Optional[int] = None,
          print_frequency=10, plot_frequency=10, save_frequency=5,
          cutoff_at=200, validation_frequency: Optional[int] = None, num_validation_trajectories=15,
          save_path: Optional[str] = None, validation_save: Optional[str] = None):
    best_mean_total_reward = -np.inf
    for epoch in range(epochs):
        agent.train()
        trajectories = [Trajectory.sample(env, agent, cutoff_at=cutoff_at) for _ in range(num_trajectories)]
        agent.train(trajectories)

        if print_frequency is not None and (epoch + 1) % print_frequency == 0:
            agent.print_progress()

        if plot_frequency is not None and (epoch + 1) % plot_frequency == 0:
            agent.plot_progress()

        if render_frequency is not None and (epoch + 1) % render_frequency == 0:
            agent.eval()
            Trajectory.sample(env, agent, cutoff_at=cutoff_at).render(env)

        if validation_frequency is not None and (epoch + 1) % validation_frequency == 0:
            agent.eval()
            validation_trajectories = [Trajectory.sample(env, agent, cutoff_at=cutoff_at) for _ in
                                       range(num_validation_trajectories)]
            mean_total_reward = np.mean([t.total_reward for t in validation_trajectories])
            log.reward(mean_total_reward, "validation mean total reward")

            if validation_save is not None and mean_total_reward > best_mean_total_reward:
                log.good(f"Better than the previous result")
                log.save(validation_save, "saving the model to ")
                best_mean_total_reward = mean_total_reward
                agent.save(validation_save)

            print()

        if save_path is not None and (epoch + 1) % save_frequency == 0:
            agent.save(save_path)


def evaluate(env: RenderableEnvironment, agent: Agent, num_trajectories=5, cutoff_at=np.inf):
    agent.eval()
    for _ in range(num_trajectories):
        t = Trajectory.sample(env, agent, cutoff_at=cutoff_at)
        t.render(env)
        log.reward(t.total_reward, "total reward")
