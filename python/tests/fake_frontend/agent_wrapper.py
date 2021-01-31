from abc import ABC, abstractmethod

import torch
from torch.distributions import Categorical

from RL.agents import Agent
from utilities import Plotter


class AgentWrapper(ABC):
    torch_device = "cuda"

    def __init__(self, env, plotter=None):
        self.state_size = env.observation_size.shape[0]
        self.action_size = env.action_size.n
        self.rollouts = []
        self.rollout_samples = []
        self.previous_state = None
        self.plotter = plotter if plotter is not None else Plotter(frequency=10)

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
        with torch.no_grad():
            self.previous_state = state
            state = torch.from_numpy(state).float().unsqueeze(0)
            logits = self.agent.actor(state)
            try:
                action = Categorical(logits=logits).sample()
            except RuntimeError as e:
                for p in self.agent.actor.parameters():
                    print(p)

                print(logits)
                raise e
            return action.item()

    def update(self) -> None:
        self.plot()
        self.agent.train(self.rollouts)
        self.rollouts = []

    @property
    @abstractmethod
    def agent(self) -> Agent:
        pass

    def plot(self):
        self.plotter.update(self.rollouts)
