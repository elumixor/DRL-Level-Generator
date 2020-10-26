from enum import Enum

import serialization
from .algorithm_type import AlgorithmType
from exceptions import ConfigurationException
from .layout_configuration import LayoutConfiguration


class NetworkType(str, Enum):
    TwoHeaded = "TwoHeaded"
    Separate = "Separate"


class AlgorithmConfiguration:
    def __init__(self, algorithm: AlgorithmType, bytes_data: bytes, start_index: int):
        total_bytes_read = 0
        if algorithm == AlgorithmType.VPG:
            self.actor_layout = LayoutConfiguration(bytes_data, start_index + total_bytes_read)
            total_bytes_read += self.actor_layout.bytes_read

        elif algorithm == AlgorithmType.A2C:
            network_type_string, bytes_read = serialization.to_string(bytes_data, start_index + total_bytes_read)
            self.network_type = NetworkType(network_type_string)
            total_bytes_read += bytes_read

            if self.network_type == NetworkType.Separate:
                self.actor_layout = LayoutConfiguration(bytes_data, start_index + total_bytes_read)
                total_bytes_read += self.actor_layout.bytes_read

                self.critic_layout = LayoutConfiguration(bytes_data, start_index + total_bytes_read)
                total_bytes_read += self.critic_layout.bytes_read

            elif self.network_type == NetworkType.TwoHeaded:
                raise ConfigurationException("Two headed network is not supported yet")
        else:
            raise ConfigurationException("Unsupported algorithm")

        self.bytes_read = total_bytes_read
