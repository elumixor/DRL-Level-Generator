from typing import List, Tuple
from unittest import TestCase

import gym
import torch

import remote_computation.logging as L
import remote_computation.model_manager as mm
from common import ByteReader
from fake_frontend.base_framework import train
from remote_computation.logging import LogOptions, LogOptionName
from remote_computation.models import ModelType, DQNModel
from remote_computation.models.remote_model import TaskType
from serialization import to_bytes


class RemoteModelLocalTests(TestCase):

    def test_obtain_works(self):
        class DQNAgentWrapper:
            torch_device = "cuda"

            def __init__(self, env, plotter=None):
                self.state_size = env.observation_space.shape[0]
                self.action_size = env.action_space.n
                self.current_trajectory = []
                self.previous_state = None

                model_dict = dict()

                b = b''
                b += to_bytes(ModelType.DQN)
                b += to_bytes(self.state_size)
                b += to_bytes(self.action_size)

                self.model: DQNModel = mm.obtain_new(model_dict, ByteReader(b))

                b = b''
                b += to_bytes(1)
                b += to_bytes(LogOptionName.TrainingLoss)

                # self.frequency = reader.read_int()
                b += to_bytes(5)
                # self.logLastN = reader.read_int()
                b += to_bytes(100)
                # self.print = reader.read_bool()
                b += to_bytes(True)
                # self.plot = reader.read_bool()
                b += to_bytes(False)
                # self.minMax = reader.read_bool()
                b += to_bytes(False)
                # self.runningAverageSmoothing = reader.read_float()
                b += to_bytes(0.8)

                self.model.log_options = LogOptions(ByteReader(b))
                self.current_trajectory: List[Tuple[List[float], List[float], float, List[float]]] = []

            def on_trajectory_started(self, state):
                pass

            def on_trajectory_finished(self) -> None:
                pass

            def save_step(self, action: int, reward: float, next_state) -> None:
                self.current_trajectory.append((self.previous_state.tolist(), [action], reward, next_state.tolist()))

            def get_action(self, state) -> int:
                with torch.no_grad():
                    self.previous_state = state
                    action = self.model.infer(state.tolist())
                    return int(action[0])

            def update(self) -> None:
                b = to_bytes(TaskType.Train)
                # num trajectories
                b += to_bytes(1)
                # num transitions in trajectory
                b += to_bytes(len(self.current_trajectory))

                for state, action, reward, next_state in self.current_trajectory:
                    b += to_bytes(state)
                    b += to_bytes(action)
                    b += to_bytes(reward)
                    b += to_bytes(next_state)

                self.model.run_task(ByteReader(b))
                L.show(self.model.log_data, self.model.log_options)
                self.current_trajectory = []

        train(gym.make('CartPole-v0'), DQNAgentWrapper, epochs=2000, num_rollouts=5, render_frequency=5)
