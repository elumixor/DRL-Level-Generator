from random import random
from typing import List, Optional

import numpy as np
import torch
import torch.nn.functional as F

from common import MemoryBuffer, setter, log
from serialization import auto_serialized, auto_saved
from .agent import Agent
from ..analysis import auto_logged, QEstimator
from ..environments import Environment, RenderableEnvironment
from ..trajectory import Trajectory
from ..utils import EpsilonDecay, MLP, map_transitions


@auto_logged("train_trajectory",
             plot_names=["loss", "epsilon", "mean_v_value", "total_reward"],
             print_names=["epsilon", "mean_v_value"])
@auto_saved
@auto_serialized
class DQNAgent(Agent, QEstimator):
    def __init__(self, env: Environment, buffer_capacity=10000, hidden_layers: Optional[List[int]] = None, lr=0.0001,
                 epsilon_decay: Optional[EpsilonDecay] = None, batch_size=200, discounting=0.99,
                 trajectories_for_evaluation=20, maximum_length=200, copy_frequency=1000):
        """
        DQN agent

        :param env: Environment
        :param hidden_layers: List of sizes of the hidden layers of the neural network
        :param buffer_capacity: Maximum capacity of the memory buffer, used for experience replay
        :param batch_size: Number of samples to be drawn from the memory buffer for one training step
        :param lr: Learning rate
        :param discounting: Discounting factor
        :param copy_frequency: Number of training steps to elapse before the target network is synchronized with the main network
        :param trajectories_for_evaluation: Number of trajectories, used to evaluate performance via average V-value
        :param maximum_length: Maximum length of the trajectory for evaluation
        """
        super().__init__(env)

        # Assign default values to the mutable parameters
        if epsilon_decay is None:
            epsilon_decay = EpsilonDecay(initial=1, end=0.1, iterations=5000)

        if hidden_layers is None:
            hidden_layers = [8, 8]

        observation_size = env.observation_size
        self.action_size = env.action_size
        self.batch_size = batch_size
        self.discount = discounting
        self.copy_frequency = copy_frequency
        self.maximum_length = maximum_length

        self.Q = MLP(observation_size, self.action_size, hidden_layers)
        self.target_Q = MLP(observation_size, self.action_size, hidden_layers)
        self.target_Q.load_state_dict(self.Q.state_dict())

        self.optim = torch.optim.Adam(self.Q.parameters(), lr=lr)

        self.memory = MemoryBuffer(capacity=buffer_capacity)
        self.epsilon = epsilon_decay

        self.loss = 0.0
        self.total_reward = 0.0
        self.mean_v_value = 0.0

        self.eval_trajectories = [self.sample_trajectory(maximum_length) for _ in range(trajectories_for_evaluation)]

        self.frame = 0

    def get_action(self, observation):
        with torch.no_grad():
            if random() < self.epsilon.value:
                return torch.randint(self.action_size, [1])

            return self.Q(observation).argmax(dim=-1, keepdim=True)

    @setter
    def eval(self, value: bool):
        if value:
            self.Q.eval()
            self.epsilon.eval()
        else:
            self.Q.train()
            self.epsilon.train()

    def train(self, epochs: int,
              render_frequency: Optional[int] = None,
              print_frequency=10, plot_frequency=10, save_frequency=5,
              validation_frequency: Optional[int] = None, num_validation_trajectories=15,
              save_path: Optional[str] = None, validation_save: Optional[str] = None):
        # Record the best mean total reward for validation and saving
        if validation_save is not None:
            best_total_reward = -np.inf

        for epoch in range(epochs):
            # Set to the training mode
            self.eval = False

            # Perform a training on trajectory and return the total reward
            self.total_reward = self.train_trajectory()

            # Print, validate, render, save regarding the frequency

            if print_frequency is not None and (epoch + 1) % print_frequency == 0:
                self.print_progress()

            if plot_frequency is not None and (epoch + 1) % plot_frequency == 0:
                self.plot_progress()

            if render_frequency is not None and (epoch + 1) % render_frequency == 0 and \
                    isinstance(self.env, RenderableEnvironment):
                self.sample_trajectory(maximum_length=self.maximum_length).render(self.env)

            if validation_frequency is not None and (epoch + 1) % validation_frequency == 0:
                self.eval = True

                # Update mean V-value
                mean_v_values = []

                for trajectory in self.eval_trajectories:
                    mean_v = self.get_trajectory_values(trajectory).mean().item()
                    mean_v_values.append(mean_v)

                self.mean_v_value = np.mean(mean_v_values)

                validation_trajectories = [self.sample_trajectory(maximum_length=self.maximum_length) for _ in
                                           range(num_validation_trajectories)]
                mean_total_reward = np.mean([t.total_reward for t in validation_trajectories])
                log.reward(mean_total_reward, "validation mean total reward")

                if validation_save is not None and mean_total_reward > best_total_reward:
                    log.good(f"Better than the previous result")
                    log.save(validation_save, "saving the model to ")
                    best_total_reward = mean_total_reward
                    self.save(validation_save)

                print()

            if save_path is not None and (epoch + 1) % save_frequency == 0:
                self.save(save_path)

    def train_trajectory(self):
        state = self.env.reset()
        observation = self.env.get_observation(state)

        total_reward = 0

        i = 0
        done = False
        while not done and i < self.maximum_length:
            action = self.get_action(observation)
            next_observation, reward, done = self.env.transition(action)

            # Put the transition into the replay buffer
            self.memory.push((observation, action, reward, done, next_observation))

            # Perform the training step if the memory is full
            if self.memory.size >= self.batch_size:
                self.loss = self.train_batch()

            total_reward += reward
            observation = next_observation
            i += 1

        return total_reward

    def train_batch(self):
        # Sample a batch of transitions from the memory buffer
        states, actions, rewards, done, next_states = map_transitions(self.memory.sample(self.batch_size))

        q = self.Q(states)
        q_selected = q[range(actions.shape[0]), actions.flatten()].flatten()

        target = rewards + self.discount * self.target_Q(next_states).max(dim=-1)[0]

        y = torch.where(done, rewards, target)

        loss = F.mse_loss(q_selected, y)

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        # Update the loss for logging
        self.loss = loss

        # Copy the parameters to the target network
        if self.frame % self.copy_frequency == 0:
            self.target_Q.load_state_dict(self.Q.state_dict())

        # Update epsilon
        self.epsilon.decay()

        return loss.item()

    def get_state_q_values(self, state: torch.Tensor) -> torch.Tensor:
        return self.Q(state)

    def get_trajectory_values(self, trajectory: Trajectory):
        states, *_ = map_transitions(trajectory)
        return self.Q(states).max(dim=-1)[0]
