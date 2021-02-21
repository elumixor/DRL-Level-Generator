from unittest import TestCase

import gym
import torch

from core import Trajectory
from core.agents import DQNAgent
from fake_frontend.base_framework import train


class RemoteModelLocalTests(TestCase):

    def test_obtain_works(self):
        class DQNAgentWrapper:
            torch_device = "cuda"

            def __init__(self, env):
                self.state_size = env.observation_space.shape[0]
                self.action_size = env.action_space.n
                env.observation_size = self.state_size
                env.action_size = self.action_size
                self.current_trajectory = Trajectory()
                self.previous_state = None
                self.agent = DQNAgent(env, trajectories_for_evaluation=0)

            def on_trajectory_started(self, state):
                pass

            def on_trajectory_finished(self) -> None:
                pass

            def save_step(self, action: int, reward: float, done, next_state) -> None:
                self.current_trajectory.append(
                    (self.previous_state, torch.tensor([action]), reward, done,
                     torch.from_numpy(next_state).to(torch.float32)))

            def get_action(self, state) -> int:
                self.previous_state = torch.from_numpy(state).to(torch.float32)
                return self.agent.get_action(self.previous_state).item()

            def update(self) -> None:
                self.agent.train([self.current_trajectory])
                self.current_trajectory = Trajectory()

            def eval(self):
                self.agent.eval()

            def train(self):
                self.agent.train()

            def plot_progress(self):
                self.agent.plot_progress()

            def print_progress(self):
                self.agent.print_progress()

        train(gym.make('CartPole-v0'), DQNAgentWrapper, epochs=2000, num_rollouts=5, render_frequency=50)
