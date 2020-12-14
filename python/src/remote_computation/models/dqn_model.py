from typing import List

import torch
import torch.nn.functional as F
from torch.nn import Sequential, Linear, ReLU

from RL import Trajectory
from common import ByteReader
from .remote_model import RemoteModel

discount = 0.99


def one_hot(x, size):
    res = torch.zeros(size)
    res[x] = 1
    return res


class DQNModel(RemoteModel):

    def __init__(self, model_id: int, reader: ByteReader):
        super().__init__(model_id, reader)

    def train(self, trajectories: List[Trajectory]):
        loss = 0

        for trajectory in trajectories:
            states, actions, rewards, next_states = zip(*trajectory)

            states = torch.tensor(states)
            actions = torch.tensor(actions)[:, [0]].long()
            rewards = torch.tensor(rewards)
            next_states = torch.tensor(next_states)

            v_next = self.nn.forward(next_states).max(dim=1, keepdim=True)[0]

            q_current = self.nn.forward(states)[actions].flatten()
            v_next = v_next.flatten()

            # Smooth l1 loss behaves like L2 near zero, but otherwise it's L1
            loss = loss + F.smooth_l1_loss(q_current, rewards + discount * v_next)

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

    def estimate_difficulty(self, trajectory: Trajectory):
        states, *_ = zip(*trajectory)
        states = torch.tensor(states)
        q = self.nn.forward(states)
        global_min, global_max = q.min(), q.max()
        q = (q - global_min) / (global_max - global_min)
        states_difficulties = q.max(dim=1)[0] - q.mean(dim=1)[0]
        return states_difficulties.mean()

    def _construct_nn(self, input_size: int, output_size: int):
        hidden_size = 5
        return Sequential(Linear(input_size, hidden_size),
                          ReLU(),
                          Linear(hidden_size, hidden_size),
                          ReLU(),
                          Linear(hidden_size, output_size))
