import torch

import serialization
from RL.agents import VPGAgent, A2CAgentSeparate, A2CAgentTwoHeaded
from configuration import TrainingConfiguration, AlgorithmType, NetworkType
from exceptions import ConfigurationException
from utilities import log, Plotter

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class TrainingController:

    def __init__(self, configuration: TrainingConfiguration):
        self.state_size = configuration.state_size
        self.action_size = 1
        self.plotter = Plotter()

        algorithm_configuration = configuration.algorithm_configuration
        if configuration.algorithm == AlgorithmType.VPG:
            self.agent = VPGAgent(algorithm_configuration.actor_layout)

        elif configuration.algorithm == AlgorithmType.A2C:
            if algorithm_configuration.network_type == NetworkType.Separate:
                self.agent = A2CAgentSeparate(algorithm_configuration.actor_layout,
                                              algorithm_configuration.critic_layout)

            elif algorithm_configuration.network_type == NetworkType.TwoHeaded:
                self.agent = A2CAgentTwoHeaded(algorithm_configuration.base_layout,
                                               algorithm_configuration.actor_head_layout,
                                               algorithm_configuration.critic_head_layout)
            else:
                raise ConfigurationException("Unsupported network type")

        log(f"Received configuration: Algorithm {configuration.algorithm}. State size: {self.state_size}. Action size: {self.action_size}")

    def train(self, training_data_bytes: bytes, start_index: int):
        training_data, _ = serialization.to_training_data(training_data_bytes, start_index, self.state_size, 1, device=device)
        self.plotter.update(training_data)
        self.agent.train(training_data)

    @property
    def actor_byte_data(self) -> bytes:
        return serialization.to_bytes(self.agent.actor.state_dict())
