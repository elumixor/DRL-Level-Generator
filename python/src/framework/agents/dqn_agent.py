from contextlib import nullcontext
from random import random
from typing import Optional, List, Callable

import torch
from torch import Tensor
from torch.nn import Module, functional as F, LeakyReLU
from torch.optim import Adam

from framework.agents import AbstractQAgent
from utils import MLP, EpsilonDecay


class DQNAgent(AbstractQAgent):
    """
    Agent that uses NN to produce Q-values. Uses an epsilon-greedy strategy to select actions
    """

    def __init__(self, state_size: int, action_size: int, hidden: Optional[List[int]] = None,
                 activation: Optional[Module] = None, optimizer_class=None, lr=0.01,
                 loss_function: Optional[Callable[[Tensor, Tensor], Tensor]] = None,
                 epsilon_initial: float = 1.0, epsilon_end: float = 0.1, epsilon_steps: int = 1000,
                 polyak_factor: float = 0.95, discount_factor: float = 0.99):
        super().__init__()

        if optimizer_class is None:
            optimizer_class = Adam

        if loss_function is None:
            loss_function = F.mse_loss

        if activation is None:
            activation = LeakyReLU()

        # Network, multi-layered perceptron
        self.nn = MLP(in_size=state_size, out_size=action_size, hidden=hidden, activation=activation)

        # Create a target network
        self.target_nn = MLP(in_size=state_size, out_size=action_size, hidden=hidden, activation=activation)

        # Copy parameters to the target network
        for p, p_target in zip(self.nn.parameters(), self.target_nn.parameters()):
            p_target.data = p.data

            # Also detach the parameter from the gradient computation
            p_target.requires_grad = False

        self.action_size = action_size
        self.epsilon = EpsilonDecay(initial=epsilon_initial, end=epsilon_end, iterations=epsilon_steps)
        self.polyak = polyak_factor
        self.discount_factor = discount_factor
        self.optim = optimizer_class(self.nn.parameters(), lr=lr)
        self.loss_function = loss_function

    def get_action(self, state: Tensor) -> Tensor:
        # With probability epsilon, select random action
        if random() < self.epsilon.value:
            return torch.randint(0, self.action_size, [1])

        # Otherwise select the action with the highest Q-value
        with torch.no_grad():
            q_values = self.nn(state)

        return torch.argmax(q_values)

    def get_q_values(self, state: Tensor, with_grad=False) -> Tensor:
        with torch.no_grad() if with_grad else nullcontext():
            return self.nn(state)

    def update(self, states: Tensor, actions: List[int], rewards: Tensor, next_states: Tensor, done: Tensor) -> float:
        q = self.nn(states)

        # Select the Q-values, that were selected (by actions)
        q = q[range(q.shape[0]), actions].unsqueeze(-1)

        # Get the Q-values for the next states using the target network
        v = torch.argmax(self.target_nn(next_states), dim=-1, keepdim=True)

        # Obtain the target for learning
        y = rewards + done * self.discount_factor * v

        loss = self.loss_function(q, y)

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        # Update target network with polyak averaging
        for p, p_target in zip(self.nn.parameters(), self.target_nn.parameters()):
            p_target.data = p_target.data * self.polyak + p.data * (1 - self.polyak)

        # Decay the epsilon
        self.epsilon.decay()

        return loss.item()
