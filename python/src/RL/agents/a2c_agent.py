from DRL.utils import nn_from_layout

from configuration.layout_configuration import LayoutConfiguration
from .vpg_agent import VPGAgent


class A2CAgent(VPGAgent):
    def __init__(self, actor_layout: LayoutConfiguration, critic_layout: LayoutConfiguration):
        super().__init__(actor_layout)
        self.critic = nn_from_layout(critic_layout)

    def train(self, training_data):
        pass
