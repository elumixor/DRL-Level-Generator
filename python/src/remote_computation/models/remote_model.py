import abc
from enum import Enum

from torch.nn import Sequential
from torch.optim import Adam

from common import ByteReader
from remote_computation.logging import LogData
from serialization import to_bytes
from .model_type import ModelType


class TaskType(int, Enum):
    Infer = 0
    Train = 1
    EstimateDifficulty = 2


class RemoteModel(abc.ABC):

    def __init__(self, model_id: int, reader: ByteReader):
        self.model_id = model_id
        self.input_size = reader.read_int()
        self.output_size = reader.read_int()
        self.nn: Sequential = self._construct_nn(self.input_size, self.output_size)
        self.optim = Adam(self.nn.parameters(), lr=0.001)
        self.log_data = LogData()

    @property
    @abc.abstractmethod
    def model_type(self) -> ModelType:
        pass

    @property
    def response_bytes(self) -> bytes:
        return to_bytes(self.model_id) + to_bytes(self.nn) + to_bytes(self.nn.state_dict())

    @property
    def save_bytes(self):
        return to_bytes(self.model_type) + \
               to_bytes(self.input_size) + \
               to_bytes(self.output_size) + \
               to_bytes(self.nn.state_dict())

    def load_from_file(self, reader: ByteReader):
        state_dict = reader.read_state_dict()
        self.nn.load_state_dict(state_dict)
        self.optim = Adam(self.nn.parameters())

    @abc.abstractmethod
    def run_task(self, reader: ByteReader) -> bytes:
        pass

    @abc.abstractmethod
    def _construct_nn(self, input_size: int, output_size: int):
        pass
