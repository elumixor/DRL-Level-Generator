import random

import numpy as np
import torch
import wandb

from core.agents import DQNAgent
from core.utils import EpsilonDecay
from environments.pendulum import PendulumEnvironment, PendulumGenerator, PendulumState
from rendering import RenderingContext

if __name__ == '__main__':
    seed = 1234

    random.seed(seed)
    torch.manual_seed(seed)
    np.random.seed(seed)

    env_name = "Pendulum"
    tests = 5

    for _ in range(tests):
        with RenderingContext(800, 600) as rc:
            class G(PendulumGenerator):
                def generate(self, difficulty: float, seed: float) -> PendulumState:
                    bob_radius = 0.15
                    max_angle = np.deg2rad(30)
                    connector_length = 0.5
                    vertical_speed = 0.02

                    enemy_radius = 0.1
                    enemy_x = -0.25 * seed + 0.25 * (1 - seed)
                    enemy_x = 0.25
                    enemy_y = 0.25

                    angle = np.deg2rad(30)
                    position = 0
                    angular_speed = np.deg2rad(5)

                    return PendulumState(bob_radius, max_angle, connector_length, vertical_speed,
                                         enemy_x, enemy_y, enemy_radius,
                                         angle, position, angular_speed)


            with PendulumEnvironment(rc, G(), difficulty=0.5) as env:
                # note: A2C
                # agent = A2CAgent(env, maximum_length=75, lr=0.001, copy_frequency=10)
                # epochs = 5000
                #
                # run = wandb.init(project="Pendulum", config={
                #     "generator.x": 0.25,
                #     "env": env_name,
                #     "seed": seed,
                #     "epochs": epochs,
                #     "max trajectory length": agent.maximum_length,
                #     "lr": agent.lr,
                #     "discounting": agent.discount,
                #     "Trajectories per epoch": agent.num_trajectories,
                #     "gradient clipping": agent.gradient_clip,
                #     "copy frequency": 10,
                # })
                # wandb.watch(agent.actor)

                # note: VPG
                # agent = VPGAgent(env, maximum_length=75, lr=0.001)
                # epochs = 5000
                #
                # run = wandb.init(project="Pendulum", config={
                #     "generator.x": 0.25,
                #     "env": env_name,
                #     "seed": seed,
                #     "epochs": epochs,
                #     "max trajectory length": agent.maximum_length,
                #     "lr": agent.lr,
                #     "discounting": agent.discount,
                #     "Trajectories per epoch": agent.num_trajectories,
                #     "gradient clipping": agent.gradient_clip
                # })
                # wandb.watch(agent.actor)

                # note: DQN
                agent = DQNAgent(env, maximum_length=75, epsilon_decay=EpsilonDecay(iterations=50000), lr=0.001,
                                 copy_frequency=500)
                epochs = 1000

                run = wandb.init(project="Pendulum", config={
                    "generator.x": 0.25,
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
