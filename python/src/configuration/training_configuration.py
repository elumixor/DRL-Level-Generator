import serialization
from .algorithm_configuration import AlgorithmConfiguration
from .algorithm_type import AlgorithmType


class TrainingConfiguration:
    def __init__(self, initial_data: bytes, start_index: int):
        algorithm, total_bytes_read = serialization.to_string(initial_data, start_index)
        self.algorithm = AlgorithmType(algorithm)

        self.algorithm_configuration = AlgorithmConfiguration(self.algorithm, initial_data, start_index + total_bytes_read)
        total_bytes_read += self.algorithm_configuration.bytes_read

        self.action_size = serialization.to_int(initial_data, start_index + total_bytes_read)
        total_bytes_read += serialization.DataTypesSize.Int

        self.state_size = serialization.to_int(initial_data, start_index + total_bytes_read)
        total_bytes_read += serialization.DataTypesSize.Int
