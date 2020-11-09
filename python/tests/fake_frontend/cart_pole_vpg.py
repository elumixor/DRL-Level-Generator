import gym

from RL.agents import VPGAgent
from configuration.nn import LayerName, IntParameter
from fake_frontend.agent_wrapper import AgentWrapper
from fake_frontend.base_framework import train
from utilities import DotDict

torch_device = "cuda"


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
    def _actor(self):
        return self.vpg


# Train, provide an env, function to get an action from state, and training function that accepts rollouts
train(gym.make('CartPole-v0'), Wrapper,
      epochs=2000, num_rollouts=5, render_frequency=None)
