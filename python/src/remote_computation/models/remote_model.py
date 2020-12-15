import abc
from enum import Enum

from torch.nn import Sequential
from torch.optim import Adam

from common import ByteReader
from serialization import to_bytes


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
        self.optim = Adam(self.nn.parameters())

    @property
    def response_bytes(self) -> bytes:
        return to_bytes(self.model_id) + to_bytes(self.nn) + to_bytes(self.nn.state_dict())

    @property
    def save_bytes(self):
        return to_bytes(self.input_size) + to_bytes(self.output_size) + to_bytes(self.nn.state_dict())

    def load_from_file(self, reader: ByteReader):
        input_size = reader.read_int()
        output_size = reader.read_int()
        self.nn = self._construct_nn(input_size, output_size)
        self.input_size = input_size
        self.output_size = output_size
        state_dict = reader.read_state_dict()
        self.nn.load_state_dict(state_dict)
        self.optim = Adam(self.nn.parameters())

    @abc.abstractmethod
    def run_task(self, reader: ByteReader) -> bytes:
        pass

    @abc.abstractmethod
    def _construct_nn(self, input_size: int, output_size: int):
        pass
