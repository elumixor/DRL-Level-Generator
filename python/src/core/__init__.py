import numpy as np

from .agents import Agent
from .environments import Environment, RenderableEnvironment
from .trajectory import Trajectory
from .utils import discounted_rewards, EpsilonDecay


def train(env: Environment, agent: Agent, epochs=100, num_trajectories=5, render_frequency=None, cutoff_at=200):
    p = 0.0
    for epoch in range(epochs):
        trajectories = [Trajectory.sample(env, agent, cutoff_at=cutoff_at) for _ in range(num_trajectories)]
        agent.update(trajectories)

        if render_frequency is not None and epoch != 0 and epoch % render_frequency == 0:
            agent.eval()
            Trajectory.sample(env, agent, cutoff_at=cutoff_at).render(env)
            agent.train()

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
