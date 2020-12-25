from random import random
from typing import List

import numpy as np
import torch
import torch.nn.functional as F
from torch.nn import Sequential, Linear, ReLU

from RL import Trajectory, State, Action, Transition
from common import ByteReader
from common.memory_buffer import MemoryBuffer
from serialization import to_bytes
from .model_type import ModelType
from .remote_model import RemoteModel, TaskType
from ..logging import LogOptionName

discount = 0.99


def one_hot(x, size):
    res = torch.zeros(size)
    res[x] = 1
    return res


def get_trajectory_total_reward(trajectory: List[Transition]):
    return sum([transition[2] for transition in trajectory])


class DQNModel(RemoteModel):

    def __init__(self, model_id: int, reader: ByteReader):
        super().__init__(model_id, reader)

        # These should probably be set from the reader
        self.train_times = 1
        self.training_batch_size = 5

        self.epsilon_initial = 1
        self.epsilon_end = 0.01
        self.epsilon_decay_epochs = 500

        # store last 2000 transitions
        self.memory = MemoryBuffer(capacity=1000)

        self.epsilon = self.epsilon_initial
        self.elapsed_epochs = 0

    @property
    def model_type(self) -> ModelType:
        return ModelType.DQN

    # todo: pass parameters such as hidden size?
    def _construct_nn(self, input_size: int, output_size: int):
        hidden_size = 32

        return Sequential(Linear(input_size, hidden_size),
                          ReLU(),
                          Linear(hidden_size, hidden_size),
                          ReLU(),
                          Linear(hidden_size, output_size))

    def run_task(self, reader: ByteReader) -> bytes:
        task = TaskType(reader.read_int())

        if task == TaskType.Infer:
            state = reader.read_list_float()
            action = self.infer(state)
            return to_bytes(action)

        if task == TaskType.Train:
            trajectories_count = reader.read_int()
            trajectory_rewards: List[float] = []

            for _ in range(trajectories_count):
                trajectory = reader.read_trajectory()
                trajectory_reward = get_trajectory_total_reward(trajectory)

                for transition in trajectory:
                    self.memory.push(transition)

                trajectory_rewards.append(trajectory_reward)

            self.log_data.add_entry(LogOptionName.TrajectoryReward,
                                    (min(trajectory_rewards), np.mean(trajectory_rewards).tolist(), max(trajectory_rewards)))

            self.train()
            return b''

        if task == TaskType.EstimateDifficulty:
            trajectory = reader.read_trajectory()
            difficulty = self.estimate_difficulty(trajectory)
            return to_bytes(difficulty)

        raise NotImplementedError()

    def infer(self, state: State) -> Action:
        if random() < self.epsilon:
            return [np.random.randint(self.output_size)]

        q = self.nn.forward(torch.tensor(state))
        return [q.squeeze().argmax().item()]

    def train(self):
        if not self.memory.is_full:
            print(f"memory is not yet full [{self.memory.size}/{self.memory.capacity}]")
            return

        losses = []

        for _ in range(self.train_times):
            transitions = self.memory.sample(self.training_batch_size)
            states, actions, rewards, next_states = zip(*transitions)

            states = torch.tensor(states)
            actions = torch.tensor(actions)[:, 0].long()
            rewards = torch.tensor(rewards)
            next_states = torch.tensor(next_states)

            # print(states)
            # print()
            # print(actions)
            # print()
            # print(rewards)
            # print()
            # print(next_states)
            # print()

            v_next = self.nn.forward(next_states).max(dim=1, keepdim=True)[0]

            # print(v_next)
            # print()
            q = self.nn.forward(states)
            # print(q)
            # print()
            q_current = q[range(actions.shape[0]), actions].flatten()
            # print(q_current)
            # print()
            v_next = v_next.flatten()
            # print(v_next)
            # print()

            # Smooth l1 loss behaves like L2 near zero, but otherwise it's L1
            loss = F.smooth_l1_loss(q_current, rewards + discount * v_next)
            loss = F.smooth_l1_loss(q_current, rewards + discount * v_next)
            # print(loss)
            # print()

            self.optim.zero_grad()
            loss.backward()
            self.optim.step()

            losses.append(loss.item())

            # exit()

        self.log_data.add_entry(LogOptionName.TrainingLoss, np.sum(losses))

        # Update epsilon
        r = max((self.epsilon_decay_epochs - self.elapsed_epochs) / self.epsilon_decay_epochs, 0.0)
        self.epsilon = (self.epsilon_initial - self.epsilon_end) * r + self.epsilon_end

        self.log_data.add_entry(LogOptionName.Epsilon, self.epsilon)

        self.elapsed_epochs += 1

    def estimate_difficulty(self, trajectory: Trajectory):
        states, *_ = zip(*trajectory)
        states = torch.tensor(states)
        q = self.nn.forward(states)
        global_min, global_max = q.min(), q.max()
        q = (q - global_min) / (global_max - global_min)
        states_difficulties = q.max(dim=1)[0] - q.mean(dim=1)[0]
        return float(states_difficulties.mean())
