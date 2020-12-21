from typing import List

import numpy as np
import torch
import torch.nn.functional as F
from torch.nn import Sequential, Linear, ReLU

from RL import Trajectory, State, Action, Transition
from common import ByteReader
from serialization import to_bytes
from .remote_model import RemoteModel, TaskType
from ..logging import LogOptionName

discount = 0.99


def one_hot(x, size):
    res = torch.zeros(size)
    res[x] = 1
    return res


def get_trajectory_data(trajectory: List[Transition]):
    _, _, rewards, _ = zip(*trajectory)
    return np.min(rewards), np.mean(rewards), np.max(rewards), len(trajectory)


class DQNModel(RemoteModel):

    def __init__(self, model_id: int, reader: ByteReader):
        super().__init__(model_id, reader)

    def _construct_nn(self, input_size: int, output_size: int):
        hidden_size = 5
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
            trajectories = []
            trajectories_count = reader.read_int()

            datas = []

            for _ in range(trajectories_count):
                trajectory = reader.read_trajectory()
                trajectories.append(trajectory)
                data = get_trajectory_data(trajectory)
                datas.append(data)

            mins, means, maxs, lengths = zip(*datas)

            self.log_data.add_entry(LogOptionName.TrajectoryReward,
                                    (np.min(mins), ((np.array(means) * np.array(lengths)).sum() / np.sum(lengths)), np.max(maxs)))

            # print(f"training... {len(transitions)} transitions received")

            # todo: NOTE: transitions are newly sampled transitions
            # todo: this is not how DQN should work
            # todo: we should add these transition into the buffer and
            # todo: then sample some random transitions
            self.train(trajectories[0])
            return b''

        if task == TaskType.EstimateDifficulty:
            trajectory = reader.read_trajectory()
            difficulty = self.estimate_difficulty(trajectory)
            return to_bytes(difficulty)

        raise NotImplementedError()

    def infer(self, state: State) -> Action:
        raise NotImplementedError()

    def train(self, transitions: List[Transition]):
        states, actions, rewards, next_states = zip(*transitions)

        print(states)
        print(actions)
        print(rewards)
        print(next_states)

        print("Now torch: ")

        states = torch.tensor(states)
        actions = torch.tensor(actions)[:, 0].long()
        rewards = torch.tensor(rewards)
        next_states = torch.tensor(next_states)

        print(states)
        print(actions)
        print(rewards)
        print(next_states)

        print("now stuff:")

        v_next = self.nn.forward(next_states).max(dim=1, keepdim=True)[0]
        q = self.nn.forward(states)
        print(q)
        q_current = self.nn.forward(states)[range(actions.shape[0]), actions].flatten()
        v_next = v_next.flatten()

        print(v_next)
        print(q_current)

        # Smooth l1 loss behaves like L2 near zero, but otherwise it's L1
        print(rewards + discount * v_next)
        loss = F.smooth_l1_loss(q_current, rewards + discount * v_next)

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        self.log_data.add_entry(LogOptionName.TrainingLoss, float(loss))

    def estimate_difficulty(self, trajectory: Trajectory):
        states, *_ = zip(*trajectory)
        states = torch.tensor(states)
        q = self.nn.forward(states)
        global_min, global_max = q.min(), q.max()
        q = (q - global_min) / (global_max - global_min)
        states_difficulties = q.max(dim=1)[0] - q.mean(dim=1)[0]
        return float(states_difficulties.mean())
