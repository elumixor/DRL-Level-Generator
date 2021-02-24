import random

import gym
import numpy as np
import torch
import wandb

from core.agents import DQNAgent
from core.utils import EpsilonDecay
from openai_env_wrapper import EnvWrapper

if __name__ == '__main__':
    seed = 1234

    random.seed(seed)
    torch.manual_seed(seed)
    np.random.seed(seed)
    env_name = "CartPole-v0"

    config = wandb.config

    env = gym.make(env_name)
    env = EnvWrapper(env)

    agent = DQNAgent(env, epsilon_decay=EpsilonDecay(iterations=50000), lr=0.001, copy_frequency=500)
    epochs = 1000

    run = wandb.init(project="Open AI. Different states", config={
        "epsilon": agent.epsilon,
        "env": env_name,
        "seed": seed,
        "epochs": epochs,
        "max trajectory length": agent.maximum_length,
        "lr": agent.lr,
        "discounting": agent.discount,
        "buffer max": agent.memory.capacity,
        "batch size": agent.batch_size,
        "target network sync frequency": agent.copy_frequency,
        "gradient clipping": agent.gradient_clip
    })

    wandb.watch(agent.Q, log="all")

    agent.train(epochs=epochs, render_frequency=25, validation_frequency=10, num_validation_trajectories=25)

    run.finish()
