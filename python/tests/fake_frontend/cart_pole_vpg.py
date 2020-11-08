import gym
import torch
from torch.distributions import Categorical

from RL.agents import VPGAgent
from configuration.nn import LayerName, IntParameter
from fake_frontend.base_framework import train
from utilities import DotDict

torch_device = "cuda"


class VPGAgentWrapper:

    def __init__(self, env):
        state_size = env.observation_space.shape[0]
        action_size = env.action_space.n
        hidden_size = 6

        config = DotDict(modules=[
                (LayerName.Linear, {IntParameter.InputSize: state_size, IntParameter.OutputSize: hidden_size}, dict()),
                (LayerName.ReLU, dict(), dict()),
                (LayerName.Linear, {IntParameter.InputSize: hidden_size, IntParameter.OutputSize: action_size}, dict()),
        ])

        self.vpg = VPGAgent(config)
        self.vpg.actor.cpu()

        self.rollouts = []
        self.rollout_samples = []
        self.previous_state = None

    def on_trajectory_started(self, state):
        pass

    def on_trajectory_finished(self) -> None:
        states, actions, rewards, next_states = zip(*self.rollout_samples)

        states = torch.stack([torch.from_numpy(s) for s in states]).float()
        next_states = torch.stack([torch.from_numpy(s) for s in next_states]).float()
        actions = torch.as_tensor(actions).unsqueeze(1)
        rewards = torch.as_tensor(rewards, dtype=torch.float).unsqueeze(1)

        self.rollouts.append((states, actions, rewards, next_states))
        self.rollout_samples = []

    def save_step(self, action: int, reward: float, next_state) -> None:
        self.rollout_samples.append((self.previous_state, action, reward, next_state))

    def get_action(self, state) -> int:
        self.previous_state = state
        state = torch.from_numpy(state).float().unsqueeze(0)
        logits = self.vpg.actor(state)
        action = Categorical(logits=logits).sample()
        return action.item()

    def update(self) -> None:
        self.vpg.train(self.rollouts)


# Train, provide an env, function to get an action from state, and training function that accepts rollouts
train(gym.make('CartPole-v0'), VPGAgentWrapper,
      epochs=2000, num_rollouts=5, print_frequency=10, plot_frequency=50, render_frequency=500)
