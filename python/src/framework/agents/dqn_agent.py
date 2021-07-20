from contextlib import nullcontext
from random import random
from typing import Optional, List, Callable

import torch
from torch import Tensor
from torch.nn import Module, functional as F, LeakyReLU
from torch.optim import Adam

from utils import MLP, EpsilonDecay, MemoryBuffer
from .abstract_q_agent import AbstractQAgent
from ..environments import AbstractEnvironment


class DQNAgent(AbstractQAgent):
    """
    Agent that uses NN to produce Q-values. Uses an epsilon-greedy strategy to select actions
    """

    def __init__(self, state_size: int, action_size: int, hidden: Optional[List[int]] = None,
                 activation: Optional[Module] = None, optimizer_class=None, lr=0.01,
                 loss_function: Optional[Callable[[Tensor, Tensor], Tensor]] = None, memory_capacity: int = 1000,
                 training_sample_size: int = 100, epsilon_initial: float = 1.0, epsilon_end: float = 0.1,
                 epsilon_steps: int = 1000, polyak_factor: float = 0.95, discount_factor: float = 0.99):
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

        self.state_size = state_size
        self.action_size = action_size
        self.activation = activation
        self.optimizer_class = optimizer_class
        self.hidden = hidden
        self.lr = lr
        self.epsilon = EpsilonDecay(initial=epsilon_initial, end=epsilon_end, iterations=epsilon_steps)
        self.polyak = polyak_factor
        self.discount_factor = discount_factor
        self.optim = optimizer_class(self.nn.parameters(), lr=lr)
        self.loss_function = loss_function
        self.memory = MemoryBuffer(capacity=memory_capacity)
        self.training_sample_size = training_sample_size

    def __copy__(self):
        result = DQNAgent(self.state_size, self.action_size, self.hidden, self.activation, type(self.optim), self.lr,
                          self.loss_function, self.memory.capacity, self.training_sample_size, self.epsilon.initial,
                          self.epsilon.end, self.epsilon.iterations, self.polyak, self.discount_factor)
        # Copy NN parameters' data
        for p_source, p_result, p_result_target in zip(self.nn.parameters(), result.nn.parameters(),
                                                       result.target_nn.parameters()):
            p_result.data = p_source.data
            p_result_target.data = p_source.data

        return result

    def get_action(self, state: Tensor) -> int:
        # With probability epsilon, select random action
        if random() < self.epsilon.value:
            return torch.randint(0, self.action_size, [1]).item()

        # Otherwise select the action with the highest Q-value
        with torch.no_grad():
            q_values = self.nn(state)

        return torch.argmax(q_values).item()

    def get_q_values(self, state: Tensor, with_grad=False) -> Tensor:
        with nullcontext() if with_grad else torch.no_grad():
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

    def train(self, environment: AbstractEnvironment, epochs: int, max_trajectory_length: int, verbose: bool = False):
        """
        Trains on a specified environment. Stops when the specified number of training iterations (epochs) has passed
        :param environment: Environment
        :param epochs: Number of training iterations to happen
        :param max_trajectory_length: Maximum length of the trajectory in an environment
        :returns Loss from the last training
        """
        if epochs < 1:
            raise Exception(f"Epochs should be at least 1, but was {epochs}")

        epoch = 0
        while True:
            # Start from the random state...
            state = environment.get_starting_state()

            # Perform a trajectory rollout
            for _ in range(max_trajectory_length):
                # Infer the action
                action = self.get_action(state)

                # Transition in environment
                next_state, reward, done = environment.transition(state, action)
                transition = state, action, reward, next_state, done

                # Push it to the memory buffer
                self.memory.push(transition)
                if self.memory.is_full:
                    # Train on the recorded transitions
                    loss = self.experience_replay()
                    if verbose:
                        print(f"Epoch {epoch + 1}/{epochs}. Loss: {loss:.5f}")

                    # Increase the epoch with this training iteration,
                    # return if the number of iterations has reached the required amount
                    epoch += 1
                    if epoch == epochs:
                        return loss

                state = next_state

                if done:
                    break

    def experience_replay(self):
        """
        Trains on the recorded transitions
        """
        states, actions, rewards, next_states, done = zip(*self.memory.sample(self.training_sample_size))

        states = torch.vstack(states)
        rewards = torch.tensor(rewards).unsqueeze(-1)
        next_states = torch.vstack(next_states)
        done = torch.tensor(done).unsqueeze(-1)

        loss = self.update(states, actions, rewards, next_states, done)

        return loss
