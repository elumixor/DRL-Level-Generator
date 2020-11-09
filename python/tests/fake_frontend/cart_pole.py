import gym

from RL.agents import VPGAgent, A2CAgentSeparate, A2CAgentTwoHeaded
from configuration.nn import LayerName, IntParameter
from fake_frontend.agent_wrapper import AgentWrapper
from fake_frontend.base_framework import train
from utilities import DotDict

torch_device = "cuda"


def vpg():
    class Wrapper(AgentWrapper):

        def __init__(self, env):
            super().__init__(env)

            hidden_size = 6

            config = DotDict(modules=[
                    (LayerName.Linear, {IntParameter.InputSize: self.state_size, IntParameter.OutputSize: hidden_size}, dict()),
                    (LayerName.ReLU, dict(), dict()),
                    (LayerName.Linear, {IntParameter.InputSize: hidden_size, IntParameter.OutputSize: self.action_size}, dict()),
            ])

            self.vpg = VPGAgent(config, lr=0.1)
            self.vpg.actor.cpu()

        @property
        def agent(self):
            return self.vpg

    train(gym.make('CartPole-v0'), Wrapper, epochs=2000, num_rollouts=5, render_frequency=None)


def a2c_separate():
    class Wrapper(AgentWrapper):

        def __init__(self, env):
            super().__init__(env)

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
            self.plotter.update(self.rollouts)

    train(gym.make('CartPole-v0'), Wrapper, epochs=2000, num_rollouts=5, render_frequency=None)


def a2c_two_headed():
    class Wrapper(AgentWrapper):

        def __init__(self, env):
            super().__init__(env)

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
            self._agent.actor.cpu()
            self._agent.critic.cpu()

        @property
        def agent(self):
            return self._agent

        def plot(self):
            self.plotter.update(self.rollouts)

    train(gym.make('CartPole-v0'), Wrapper, epochs=2000, num_rollouts=5, render_frequency=None)


a2c_two_headed()
