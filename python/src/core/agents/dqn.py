from typing import List
from random import random

import numpy as np
import torch
import torch.nn.functional as F

from common import MemoryBuffer
from .agent import Agent
from ..environments import Environment
from ..utils import EpsilonDecay, MLP, map_transitions
from ..trajectory import Trajectory


class DQNAgent(Agent):
    def __init__(self, env: Environment, buffer_capacity=1000, hidden_sizes=None, lr=0.01, epsilon_initial=1,
                 epsilon_end=0.01, epsilon_iterations=500, batch_size=100, discount=0.99):
        if hidden_sizes is None:
            hidden_sizes = [8, 8]

        observation_size = env.observation_size
        self.action_size = env.action_size

        self.Q = MLP(observation_size, self.action_size, hidden_sizes)
        self.optim = torch.optim.Adam(self.Q.parameters(), lr=lr)

        self.memory = MemoryBuffer(capacity=buffer_capacity)

        self.batch_size = batch_size

        self.discount = discount
        self.epsilon = EpsilonDecay(initial=epsilon_initial, end=epsilon_end, iterations=epsilon_iterations)

    def get_action(self, observation):
        if random() < self.epsilon.value:
            return torch.randint(self.action_size, [1])

        return self.Q(observation).argmax(dim=-1, keepdim=True)

    def train(self, trajectories: List[Trajectory]):
        # Add transitions to the memory buffer
        total_rewards = []
        for trajectory in trajectories:
            for transition in trajectory:
                self.memory.push(transition)

                # Sample transitions from the buffer
                if not self.memory.is_full:
                    print(f"memory is not yet full [{self.memory.size}/{self.memory.capacity}]")
                    continue

                transitions = self.memory.sample(self.batch_size)
                states, actions, rewards, done, next_states = map_transitions(transitions)

                # Main training function for the batch
                self._train_batch(states, actions, rewards, done, next_states)

            total_rewards.append(trajectory.total_reward)

        print(f"Mean total trajectory reward {np.mean(total_rewards)}")

        self.epsilon.decay()

    def eval(self):
        self.Q.eval()
        self.epsilon.eval()

    def _train_batch(self, states, actions, rewards, done, next_states):
        """
        Performs an update over a batch of transitions
        :returns: Loss of the batch
        """
        v_next = self.Q.forward(next_states).max(dim=1, keepdim=True)[0]
        q = self.Q.forward(states)
        q_current = q[range(actions.shape[0]), actions[:, 0]].flatten()
        v_next = v_next.flatten()
        v_next[done] = rewards[done].to(torch.float32)

        # Smooth l1 loss behaves like L2 near zero, but otherwise it's L1
        loss = F.smooth_l1_loss(q_current, rewards + self.discount * v_next)

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        return loss
