import torch

from RL.agents import VPGAgent
from configuration.nn import LayerName, IntParameter
from fake_frontend.agent_wrapper import AgentWrapper
from fake_frontend.base_framework import train
from fake_frontend.environments import LeftRightEnvironment
from utilities import DotDict, np
from utilities.logging.left_right_plotter import LeftRightPlotter

torch_device = "cuda"


class Wrapper(AgentWrapper):

    def __init__(self, env):
        super().__init__(env, plotter=LeftRightPlotter(frequency=20))

        hidden_size = 6

        config = DotDict(modules=[
                (LayerName.Linear, {IntParameter.InputSize: self.state_size, IntParameter.OutputSize: hidden_size}, dict()),
                (LayerName.ReLU, dict(), dict()),
                (LayerName.Linear, {IntParameter.InputSize: hidden_size, IntParameter.OutputSize: self.action_size}, dict()),
        ])

        self.vpg = VPGAgent(config)
        self.vpg.actor.cpu()

    @property
    def _actor(self):
        return self.vpg

    def plot(self):
        # Also plot the probability of going left
        x = np.linspace(-5, 5, 100)
        p_left_x = self._actor.actor(torch.from_numpy(x).float().unsqueeze(-1)) \
                       .softmax(-1)[:, 0].detach().numpy()
        self.plotter.update(self.rollouts, p_left_x=(x, p_left_x))


# Train, provide an env, function to get an action from state, and training function that accepts rollouts
train(LeftRightEnvironment(), Wrapper,
      epochs=2000, num_rollouts=5, render_frequency=False, max_timesteps=20)
