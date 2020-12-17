from typing import List

import torch
import torch.nn.functional as F
from torch.nn import Sequential, Linear, ReLU

from RL import Trajectory, State, Action, Transition
from common import ByteReader
from serialization import to_bytes
from .remote_model import RemoteModel, TaskType

discount = 0.99


def one_hot(x, size):
    res = torch.zeros(size)
    res[x] = 1
    return res


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
            transitions = []
            transitions_count = reader.read_int()

            for _ in range(transitions_count):
                transition = reader.read_transition()
                transitions.append(transition)

            self.train(transitions)
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

        states = torch.tensor(states)
        actions = torch.tensor(actions)[:, [0]].long()
        rewards = torch.tensor(rewards)
        next_states = torch.tensor(next_states)

        v_next = self.nn.forward(next_states).max(dim=1, keepdim=True)[0]

        q_current = self.nn.forward(states)[actions].flatten()
        v_next = v_next.flatten()

        # Smooth l1 loss behaves like L2 near zero, but otherwise it's L1
        loss = F.smooth_l1_loss(q_current, rewards + discount * v_next)

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
        return float(states_difficulties.mean())
