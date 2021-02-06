from random import random
from typing import List

import numpy as np
import torch
import torch.nn.functional as F

from common import MemoryBuffer
from .agent import Agent
from ..analysis import Logged
from ..environments import Environment
from ..trajectory import Trajectory
from ..utils import EpsilonDecay, MLP, map_transitions


@Logged(plot_names=["loss", "epsilon", "mean_q_value", "mean_total_reward"], print_names=["epsilon", "mean_q_value"])
class DQNAgent(Agent):
    def __init__(self, env: Environment, buffer_capacity=10000, hidden_sizes=None, lr=0.01, epsilon_initial=1,
                 epsilon_end=0.1, epsilon_iterations=500, batch_size=200, discount=0.99,
                 trajectories_for_evaluation=20, cutoff_at=200):
        if hidden_sizes is None:
            hidden_sizes = [8, 8]

        observation_size = env.observation_size
        self.action_size = env.action_size

        self.Q = MLP(observation_size, self.action_size, hidden_sizes)
        self.optim = torch.optim.Adam(self.Q.parameters(), lr=lr)

        self.memory = MemoryBuffer(capacity=buffer_capacity)

        self.batch_size = batch_size

        self.discount = discount
        self._epsilon = EpsilonDecay(initial=epsilon_initial, end=epsilon_end, iterations=epsilon_iterations)

        self.loss = 0.0
        self.mean_total_reward = 0.0
        self.mean_q_value = 0.0

        self._trajectories_for_q_evaluation = [Trajectory.sample(env, self, cutoff_at) for _ in
                                               range(trajectories_for_evaluation)]

    @property
    def epsilon(self):
        return self._epsilon.value

    def get_action(self, observation):
        if random() < self._epsilon.value:
            return torch.randint(self.action_size, [1])

        return self.Q(observation).argmax(dim=-1, keepdim=True)

    def update(self, trajectories: List[Trajectory]):
        # Add transitions to the memory buffer
        total_rewards = []

        self.loss = 0

        for trajectory in trajectories:
            for transition in trajectory:
                self.memory.push(transition)

                if self.memory.size < self.batch_size:
                    continue

                transitions = self.memory.sample(self.batch_size)
                states, actions, rewards, done, next_states = map_transitions(transitions)

                # Main training function for the batch
                self.loss += self._train_batch(states, actions, rewards, done, next_states)

            total_rewards.append(trajectory.total_reward)

        self.mean_total_reward = np.mean(total_rewards)
        self._update_mean_q()

        self._epsilon.decay()

    def eval(self):
        self.Q.eval()
        self._epsilon.eval()

    def train(self):
        self.Q.train()
        self._epsilon.train()

    def _train_batch(self, states, actions, rewards, done, next_states):
        """
        Performs an update over a batch of transitions
        :returns: Loss of the batch
        """
        v_next = self.Q.forward(next_states).max(dim=1)[0]
        q = self.Q.forward(states)
        q_current = q[range(actions.shape[0]), actions.flatten()].flatten()

        y = rewards + self.discount * v_next
        y = torch.where(done, rewards, y)

        loss = F.mse_loss(q_current, y)

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        return loss

    def _update_mean_q(self):
        mean_q_values = []
        for transitions in self._trajectories_for_q_evaluation:
            states, *_ = map_transitions(transitions)
            q = self.Q.forward(states)
            mean_q = q.max(dim=-1)[0].mean().item()
            mean_q_values.append(mean_q)

        self.mean_q_value = np.mean(mean_q_values)
