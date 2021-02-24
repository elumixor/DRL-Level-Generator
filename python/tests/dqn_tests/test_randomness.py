import random

import gym
import numpy as np
import torch
import wandb

from core.agents import DQNAgent
from core.utils import EpsilonDecay
from openai_env_wrapper import EnvWrapper

if __name__ == '__main__':

    for _ in range(10):
        random.seed(1234)
        torch.manual_seed(1234)
        np.random.seed(0)

        run = wandb.init(project="Randomness")

        config = wandb.config

        env = gym.make('CartPole-v0')
        env.seed(1234)
        env = EnvWrapper(env)

        agent = DQNAgent(env, epsilon_decay=EpsilonDecay(iterations=50000))

        agent.train(epochs=100, render_frequency=25, validation_frequency=10, num_validation_trajectories=25)

        run.finish()
