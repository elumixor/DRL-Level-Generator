import torch
from RL.agents import VPGAgent, A2CAgentSeparate, A2CAgentTwoHeaded
from configuration.nn import LayerName, IntParameter

from environments import LeftRightEnvironment
from fake_frontend.agent_wrapper import AgentWrapper
from fake_frontend.base_framework import train
from utilities import DotDict, np
from utilities.logging.left_right_plotter import LeftRightPlotter

torch_device = "cuda"

env = LeftRightEnvironment()


def vpg():
    class Wrapper(AgentWrapper):

        def __init__(self, env):
            super().__init__(env, plotter=LeftRightPlotter(frequency=20))

            hidden_size = 6

            config = DotDict(modules=[
                    (LayerName.Linear, {IntParameter.InputSize: self.state_size, IntParameter.OutputSize: hidden_size}, dict()),
                    (LayerName.ReLU, dict(), dict()),
                    (LayerName.Linear, {IntParameter.InputSize: hidden_size, IntParameter.OutputSize: self.action_size}, dict()),
            ])

            self._agent = VPGAgent(config)
            self.agent.actor.cpu()

        @property
        def agent(self):
            return self._agent

        def plot(self):
            # Also plot the probability of going left
            x = np.linspace(-5, 5, 100)
            p_left_x = self.agent.actor(torch.from_numpy(x).float().unsqueeze(-1)) \
                           .softmax(-1)[:, 0].detach().numpy()
            self.plotter.train(self.rollouts, p_left_x=(x, p_left_x))

    train(env, Wrapper, epochs=2000, num_rollouts=5, render_frequency=False, max_timesteps=20)


def a2c_separate():
    class Wrapper(AgentWrapper):

        def __init__(self, env):
            super().__init__(env, plotter=LeftRightPlotter(frequency=20))

            hidden_size = 6

            actor_layout = DotDict(modules=[
                    (LayerName.Linear, {IntParameter.InputSize: self.state_size, IntParameter.OutputSize: hidden_size}, dict()),
                    (LayerName.ReLU, dict(), dict()),
                    (LayerName.Linear, {IntParameter.InputSize: hidden_size, IntParameter.OutputSize: self.action_size}, dict()),
            ])

            critic_layout = DotDict(modules=[
                    (LayerName.Linear, {IntParameter.InputSize: self.state_size, IntParameter.OutputSize: hidden_size}, dict()),
                    (LayerName.ReLU, dict(), dict()),
                    (LayerName.Linear, {IntParameter.InputSize: hidden_size, IntParameter.OutputSize: 1}, dict()),
            ])

            self._agent = A2CAgentSeparate(actor_layout, critic_layout, 0.025, 0.001)
            self._agent.actor.cpu()
            self._agent.critic.cpu()

        @property
        def agent(self):
            return self._agent

        def plot(self):
            # Also plot the probability of going left
            x = np.linspace(-5, 5, 100)
            p_left_x = self.agent.actor(torch.from_numpy(x).float().unsqueeze(-1)) \
                           .softmax(-1)[:, 0].detach().numpy()
            self.plotter.train(self.rollouts, p_left_x=(x, p_left_x))

    # Train, provide an env, function to get an action from state, and training function that accepts rollouts
    train(env, Wrapper, epochs=2000, num_rollouts=5, render_frequency=False, max_timesteps=20)


def a2c_two_headed():
    class Wrapper(AgentWrapper):

        def __init__(self, env):
            super().__init__(env, plotter=LeftRightPlotter(frequency=20))

            hidden_size = 6

            base_layout = DotDict(modules=[
                    (LayerName.Linear, {IntParameter.InputSize: self.state_size, IntParameter.OutputSize: hidden_size}, dict()),
                    (LayerName.ReLU, dict(), dict()),
            ])

            actor_layout = DotDict(modules=[
                    (LayerName.Linear, {IntParameter.InputSize: hidden_size, IntParameter.OutputSize: self.action_size}, dict()),
            ])

            critic_layout = DotDict(modules=[
                    (LayerName.Linear, {IntParameter.InputSize: hidden_size, IntParameter.OutputSize: 1}, dict()),
            ])

            self._agent = A2CAgentTwoHeaded(base_layout, actor_layout, critic_layout, 0.025)
            self._agent.actor_head.cpu()
            self._agent.critic_head.cpu()
            self._agent.base.cpu()
            self._agent.actor.cpu()
            self._agent.critic.cpu()

        @property
        def agent(self):
            return self._agent

        def plot(self):
            # Also plot the probability of going left
            x = np.linspace(-5, 5, 100)
            p_left_x = self.agent.actor(torch.from_numpy(x).float().unsqueeze(-1)) \
                           .softmax(-1)[:, 0].detach().numpy()
            self.plotter.train(self.rollouts, p_left_x=(x, p_left_x))

    # Train, provide an env, function to get an action from state, and training function that accepts rollouts
    train(env, Wrapper,
          epochs=2000, num_rollouts=5, render_frequency=False, max_timesteps=20)


a2c_two_headed()
