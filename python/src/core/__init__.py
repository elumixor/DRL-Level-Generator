import time

import numpy as np

from .agents import Agent
from .environments import Environment, RenderableEnvironment
from .utils import discounted_rewards, EpsilonDecay


def sample_trajectory(env: Environment, agent: Agent, max_length=np.inf):
    state = env.reset()
    observation = env.get_observation(state)

    trajectory = []

    i = 0
    done = False
    while not done and i < max_length:
        action = agent.get_action(observation)
        next_state, reward, done = env.transition(action)
        next_observation = env.get_observation(next_state)

        trajectory.append((observation, action, reward, done, next_observation))
        observation = next_observation
        i += 1

    return trajectory


def render_trajectory(env: RenderableEnvironment, trajectory, delta_time=0.02):
    for state, *_ in trajectory:
        env.set_state(state)
        env.render()
        time.sleep(delta_time)


def train(env: Environment, agent: Agent, epochs, num_trajectories, render):
    for epoch in range(epochs):
        trajectories = [sample_trajectory(env, agent, max_length=75) for _ in range(num_trajectories)]
        agent.train(trajectories)

        # todo: log data

        if epoch != 0 and epochs % render:
            render_trajectory(env, sample_trajectory(env, agent))
