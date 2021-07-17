from typing import Optional, List, Callable

import torch
from torch import Tensor
from torch.distributions import Categorical
from torch.nn import Module, functional as F, LeakyReLU
from torch.optim import Adam

from utils import MLP
from .abstract_agent import AbstractAgent


class PGAgent(AbstractAgent):
    """
    Policy gradient agent that provides a probability distribution over states
    """

    def __init__(self, state_size: int, action_size: int, hidden: Optional[List[int]] = None,
                 activation: Optional[Module] = None, optimizer_class=None, lr=0.01,
                 loss_function: Optional[Callable[[Tensor, Tensor], Tensor]] = None,
                 discount_factor: float = 0.99):
        if optimizer_class is None:
            optimizer_class = Adam

        if loss_function is None:
            loss_function = F.mse_loss

        if activation is None:
            activation = LeakyReLU()

        # Network, multi-layered perceptron
        self.nn = MLP(in_size=state_size, out_size=action_size, hidden=hidden, activation=activation)
        self.action_size = action_size
        self.discount_factor = discount_factor
        self.optim = optimizer_class(self.nn.parameters(), lr=lr)
        self.loss_function = loss_function

    def get_action(self, state: Tensor) -> Tensor:
        with torch.no_grad():
            logits = self.nn(state)
            distribution = Categorical(logits=logits)
            return distribution.sample()

    def get_state_difficulty(self, state: Tensor) -> Tensor:
        """
        Returns the difficulty of the given state as the difference
        between the maximum and the mean probability over the state actions
        :param state: State
        :return: Difficulty, shape (num_states, num_actions)
        """
        with torch.no_grad():
            logits = self.nn(state)
            probabilities = F.softmax(logits, dim=-1)
            return probabilities.max(dim=-1) - probabilities.min(dim=-1)

    def update(self, states: Tensor, actions: List[int], rewards: Tensor) -> float:
        # print("rewards")
        # print(rewards)
        # print()

        # Get the probabilities for the actions in the states
        logits = self.nn(states)
        # print("logits")
        # print(logits)
        # print()

        # Select the ones, that correspond to the selected actions
        logits = logits[range(logits.shape[0]), actions].unsqueeze(-1)
        # print("selected logits")
        # print(logits)
        # print()

        loss = -(logits * rewards).mean()

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        return loss.item()
