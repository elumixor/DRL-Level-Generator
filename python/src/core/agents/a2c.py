from copy import deepcopy
from typing import Optional

import numpy as np
import torch
import wandb

from common import log, MLP
from serialization import auto_saved, auto_serialized
from .agent import Agent
from ..environments import RenderableEnvironment
from ..trajectory import Trajectory
from ..utils import map_transitions


@auto_saved
@auto_serialized(skip=["base", "actor_head", "critic_head"])
class A2CAgent(Agent):
    def __init__(self, env, hidden_sizes=None, lr=0.01, discount=0.99, num_trajectories=10,
                 actor_loss_weight=1, critic_loss_weight=0.5, entropy_loss_weight=0.0001,
                 trajectories_for_evaluation=20, copy_frequency=500, maximum_length=75, gradient_clip=float("inf")
                 ):
        super().__init__(env)

        if hidden_sizes is None:
            hidden_sizes = [8, 6]

        # Build the network
        observation_size = env.observation_size
        self.action_size = env.action_size

        last_size = observation_size
        # if len(hidden_sizes) > 0:
        #     last_size = hidden_sizes[-1]
        #     self.base = MLP(observation_size, last_size, hidden_sizes[:-1])
        # else:
        #     self.base = Identity()

        # self.actor_head = Linear(last_size, self.action_size)
        # self.critic_head = Linear(last_size, 1)

        # self.actor = Sequential(self.base, ReLU(), self.actor_head)
        # self.critic = Sequential(self.base, ReLU(), self.critic_head)

        self.actor = MLP(observation_size, self.action_size, [8, 8])
        self.critic = MLP(observation_size, 1, [8, 8])

        self.critic_target = deepcopy(self.critic)

        self.parameters = [*self.actor.parameters(), *self.critic.parameters()]

        self.optim = torch.optim.Adam(self.parameters, lr=lr)

        self.lr = lr
        self.discount = discount
        self.num_trajectories = num_trajectories
        self.critic_loss_weight = critic_loss_weight
        self.entropy_loss_weight = entropy_loss_weight
        self.actor_loss_weight = actor_loss_weight
        self.maximum_length = maximum_length
        self.gradient_clip = gradient_clip
        self.copy_frequency = copy_frequency

        with torch.no_grad():
            self.eval_trajectories = [self.sample_trajectory(maximum_length) for _ in
                                      range(trajectories_for_evaluation)]

        self.frame = 0

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
                mean_v_values = []

                for trajectory in self.eval_trajectories:
                    mean_v = self.get_trajectory_values(trajectory).mean().item()
                    mean_v_values.append(mean_v)

                wandb.log({"mean V": np.mean(mean_v_values)})

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

        total_len = 0
        total_reward = 0.0

        loss_actor = 0.0
        loss_critic = 0.0
        entropy_loss = 0.0

        for trajectory in trajectories:
            states, actions, rewards, done, next_states = map_transitions(trajectory)

            v = self.critic(states).flatten()
            v_next = self.critic_target(next_states).flatten().detach()

            G = rewards + self.discount * v_next
            advantages = G - v
            loss_critic = loss_critic + (advantages ** 2).sum()

            probabilities = self.actor(states).softmax(-1) + 1e-5
            selected_probabilities = probabilities[range(actions.shape[0]), actions.flatten()]
            loss_actor = loss_actor - (selected_probabilities.log() * advantages.flatten().detach()).sum()

            entropy_loss = entropy_loss + (probabilities * probabilities.log()).sum()

            total_len += states.shape[0]
            total_reward += rewards.sum().item()

        loss_actor = loss_actor / total_len
        loss_critic = loss_critic / total_len
        entropy_loss = entropy_loss / total_len

        loss = self.actor_loss_weight * loss_actor + \
               self.critic_loss_weight * loss_critic + \
               self.entropy_loss_weight * entropy_loss

        self.optim.zero_grad()
        loss.backward()

        # Compute the gradients' norm
        norms = []
        for p in self.parameters:
            norms.append(p.grad.data.norm(2).cpu().item())

        wandb.log({
            "gradient norm (average)": np.mean(norms),
            "gradient norm (sum)": sum(norms),
            "gradient norm (max)": max(norms)
        })

        # Clip the norm
        torch.nn.utils.clip_grad_norm_(self.parameters, self.gradient_clip)

        self.optim.step()

        # Copy the parameters to the target network
        if self.frame != 0 and self.frame % self.copy_frequency == 0:
            self.critic_target = deepcopy(self.critic)

        self.frame += 1

        wandb.log({"loss": loss.item(), "Episode reward": total_reward / self.num_trajectories})

    def get_trajectory_values(self, trajectory: Trajectory):
        states, *_ = map_transitions(trajectory)
        return self.critic(states)
