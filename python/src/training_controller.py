import torch

import DRL.agents
import serialization
from configuration import TrainingConfiguration, AlgorithmType
from utilities import log

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class TrainingController:
    def __init__(self, configuration: TrainingConfiguration):
        self.state_size = configuration.state_size
        self.action_size = configuration.action_size
        self.transition_size = 2 * self.state_size + self.action_size + 1

        if configuration.algorithm == AlgorithmType.VPG:
            self.agent = DRL.agents.VPGAgent(configuration.algorithm_configuration.actor_layout)
        elif configuration.algorithm == AlgorithmType.A2C:
            self.agent = DRL.agents.A2CAgent(configuration.algorithm_configuration.actor_layout,
                                             configuration.algorithm_configuration.critic_layout)
        log(f"Received configuration: Algorithm {configuration.algorithm}. State size: {self.state_size}. Action size: {self.action_size}")

    def train(self, training_data_bytes: bytes, start_index: int):
        training_data, _ = serialization.to_training_data(training_data_bytes, start_index, self.state_size, self.action_size,
                                                          device=device)
        self.agent.train(training_data)

    @property
    def actor_byte_data(self) -> bytes:
        return serialization.to_bytes(self.agent.actor.state_dict())
