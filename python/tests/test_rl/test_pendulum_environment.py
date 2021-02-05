import time
from abc import abstractmethod, ABC
from random import random

import numpy as np
import torch

from RL import EpsilonDecay
from common.memory_buffer import MemoryBuffer
from environments import PendulumEnvironment, BaseEnvironment
from environments.pendulum import configurations2parameters, PendulumStaticConfiguration, EnemyStaticConfiguration, \
    PendulumDynamicConfiguration, EnemyDynamicConfiguration
from environments.renderable_environment import RenderableEnvironment
from rendering import RenderingContext
from utilities import MLP
import torch.nn.functional as F

if __name__ == '__main__':
    with RenderingContext(800, 600) as rc:
        with PendulumEnvironment(rc) as env:
            pendulum_static_configuration = PendulumStaticConfiguration(0.35, np.deg2rad(30), 0.5, 0.02)
            pendulum_dynamic_configuration = PendulumDynamicConfiguration(np.deg2rad(30), 0, np.deg2rad(5))

            enemies_static_configurations = [EnemyStaticConfiguration(0.25, 0.25, 0.25)]
            enemies_dynamic_configurations = [EnemyDynamicConfiguration()]

            generated_parameters = configurations2parameters(pendulum_static_configuration,
                                                             enemies_static_configurations,
                                                             pendulum_dynamic_configuration,
                                                             enemies_dynamic_configurations)
            env.setup(generated_parameters)


            # Now we have a configured environment to train on

            class Agent(ABC):
                @abstractmethod
                def get_action(self, observation):
                    ...

                @abstractmethod
                def train(self, trajectories):
                    pass


            class DQNAgent(Agent):
                def __init__(self, env: BaseEnvironment):
                    observation_size = env.observation_size
                    self.action_size = env.action_size

                    self.epsilon = EpsilonDecay()

                    # State size to action
                    self.Q = MLP(observation_size, self.action_size, [8, 8])

                    self.optim = torch.optim.Adam(self.Q.parameters(), lr=0.01)

                    self.memory = MemoryBuffer(capacity=1000)
                    self.batches = 5
                    self.batch_size = 100

                    self.discount = 0.99

                def get_action(self, observation):
                    if random() < self.epsilon.value:
                        return torch.randint(self.action_size, [1])

                    return self.Q(observation).argmax

                def train(self, trajectories):
                    # Add transitions to the memory buffer
                    for trajectory in trajectories:
                        for transition in trajectory:
                            self.memory.push(transition)

                    # Sample transitions from the buffer
                    if not self.memory.is_full:
                        print(f"memory is not yet full [{self.memory.size}/{self.memory.capacity}]")
                        return

                    losses = []

                    for _ in range(self.batches):
                        transitions = self.memory.sample(self.batch_size)
                        states, actions, rewards, next_states = zip(*transitions)

                        # todo: add Done

                        states = torch.stack(states)
                        actions = torch.stack(actions)
                        rewards = torch.tensor(rewards)
                        next_states = torch.stack(next_states)

                        v_next = self.Q.forward(next_states).max(dim=1, keepdim=True)[0]
                        q = self.Q.forward(states)
                        q_current = q[range(actions.shape[0]), actions[:, 0]].flatten()
                        v_next = v_next.flatten()

                        # Smooth l1 loss behaves like L2 near zero, but otherwise it's L1
                        loss = F.smooth_l1_loss(q_current, rewards + self.discount * v_next)

                        self.optim.zero_grad()
                        loss.backward()
                        self.optim.step()

                        losses.append(loss.item())

                    print(np.sum(losses))

                    self.epsilon.decay()


            def sample_trajectory(env: BaseEnvironment, agent: Agent):
                state = env.reset()
                observation = env.get_observation(state)

                trajectory = []

                done = False
                while not done:
                    action = agent.get_action(observation)
                    next_state, reward, done = env.transition(action)
                    next_observation = env.get_observation(next_state)

                    trajectory.append((observation, action, reward, next_observation))
                    observation = next_observation

                return trajectory


            def render_trajectory(env: RenderableEnvironment, trajectory, delta_time=0.1):
                for state, *_ in trajectory:
                    env.set_state(state)
                    env.render()
                    time.sleep(delta_time)


            def train(env: BaseEnvironment, agent: Agent, epochs, num_trajectories, render):
                for epoch in range(epochs):
                    trajectories = [sample_trajectory(env, agent) for _ in range(num_trajectories)]
                    agent.train(trajectories)

                    # todo: log data

                    if epoch != 0 and epochs % render:
                        render_trajectory(env, sample_trajectory(env, agent))


            agent = DQNAgent(env)
            train(env, agent, epochs=200, num_trajectories=10, render=25)

            for _ in range(50):
                trajectory = sample_trajectory(env, agent)
                render_trajectory(env, trajectory)
