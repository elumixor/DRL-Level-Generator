from typing import Optional

import torch
import wandb
from wandb.util import np

from common import log, MLP
from serialization import auto_serialized, auto_saved
from .agent import Agent
from ..environments import Environment, RenderableEnvironment
from ..utils import map_transitions, discounted_rewards


@auto_saved
@auto_serialized
class VPGAgent(Agent):
    def __init__(self, env: Environment, hidden_sizes=None, lr=0.01, discount=0.99, num_trajectories=10,
                 maximum_length=75, gradient_clip=float("inf")):
        super().__init__(env)

        observation_size = env.observation_size
        self.action_size = env.action_size
        self.num_trajectories = num_trajectories
        self.discount = discount
        self.maximum_length = maximum_length
        self.lr = lr
        self.gradient_clip = gradient_clip

        if hidden_sizes is None:
            hidden_sizes = [8, 8]

        self.actor = MLP(observation_size, self.action_size, hidden_sizes)
        self.optim = torch.optim.Adam(self.actor.parameters(), lr=lr)

    def get_action(self, observation):
        with torch.no_grad():
            logits = self.actor(observation)
            distribution = torch.distributions.Categorical(logits=logits)
            action = distribution.sample([1])
            return action

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
            self.train_epoch()

            # Print, validate, render, save regarding the frequency
            if render_frequency is not None and (epoch + 1) % render_frequency == 0 and \
                    isinstance(self.env, RenderableEnvironment):
                self.sample_trajectory(maximum_length=self.maximum_length).render(self.env)

            if validation_frequency is not None and (epoch + 1) % validation_frequency == 0:
                self.eval = True

                # Update mean V-value
                validation_trajectories = [self.sample_trajectory(maximum_length=self.maximum_length) for _ in
                                           range(num_validation_trajectories)]
                mean_total_reward = np.mean([t.total_reward for t in validation_trajectories])
                log.reward(mean_total_reward, "validation mean total reward")

                wandb.log({"validation total reward": mean_total_reward})

                if validation_save is not None and mean_total_reward > best_total_reward:
                    log.good(f"Better than the previous result")
                    log.save(validation_save, "saving the model to ")
                    best_total_reward = mean_total_reward
                    self.save(validation_save)

                print()

            if save_path is not None and (epoch + 1) % save_frequency == 0:
                self.save(save_path)

            wandb.log({"epoch": epoch})

    def train_epoch(self):
        trajectories = [self.sample_trajectory(self.maximum_length) for _ in range(self.num_trajectories)]

        loss = 0.0
        total_len = 0
        total_reward = 0.0

        for trajectory in trajectories:
            states, actions, rewards, done, next_states = map_transitions(trajectory)

            _discounted_rewards = discounted_rewards(rewards, self.discount).flatten()

            probabilities = self.actor(states).softmax(-1)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss = loss - (probabilities.log() * _discounted_rewards).sum()

            total_len += _discounted_rewards.shape[0]
            total_reward += rewards.sum().item()

        loss = loss / total_len

        self.optim.zero_grad()
        loss.backward()

        # Compute the gradients' norm
        norms = []
        for p in self.actor.parameters():
            norms.append(p.grad.data.norm(2).cpu().item())

        wandb.log({
            "gradient norm (average)": np.mean(norms),
            "gradient norm (sum)": sum(norms),
            "gradient norm (max)": max(norms)
        })

        # Clip the norm
        torch.nn.utils.clip_grad_norm_(self.actor.parameters(), self.gradient_clip)

        self.optim.step()

        wandb.log({"loss": loss.item(), "mean_total_reward": total_reward / self.num_trajectories})
