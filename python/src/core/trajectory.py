from __future__ import annotations

import time

import numpy as np

from .agents import Agent
from .environments import Environment, RenderableEnvironment


class Trajectory(list):
    @staticmethod
    def sample(env: Environment, agent: Agent, cutoff_at=np.inf) -> Trajectory:
        state = env.reset()
        observation = env.get_observation(state)

        trajectory = Trajectory()

        i = 0
        done = False
        while not done and i < cutoff_at:
            action = agent.get_action(observation)
            next_state, reward, done = env.transition(action)
            next_observation = env.get_observation(next_state)

            trajectory.append((observation, action, reward, done, next_observation))
            observation = next_observation
            i += 1

        return trajectory

    @property
    def total_reward(self):
        return sum([reward for _, _, reward, _, _, in self])

    def render(self, env: RenderableEnvironment, delta_time=1 / 60):
        for state, *_ in self:
            env.set_state(state)
            env.render()
            time.sleep(delta_time)
