import abc
from enum import Enum
from typing import List

from torch.nn import Sequential
from torch.optim import Adam

from RL import State, Action, Trajectory
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

    def run_task(self, reader: ByteReader) -> bytes:
        task = TaskType(reader.read_int())

        if task == TaskType.Infer:
            state = reader.read_list_float()
            action = self.infer(state)
            return to_bytes(action)

        if task == TaskType.Train:
            trajectories_count = reader.read_int()
            trajectories = []

            for _ in range(trajectories_count):
                trajectory = reader.read_trajectory()
                trajectories.append(trajectory)

            self.train(trajectories)
            return b''

        if task == TaskType.EstimateDifficulty:
            trajectory = reader.read_trajectory()
            self.estimate_difficulty(trajectory)

    @abc.abstractmethod
    def _construct_nn(self, input_size: int, output_size: int):
        pass

    def infer(self, state: State) -> Action:
        raise NotImplementedError()

    def train(self, trajectories: List[Trajectory]):
        raise NotImplementedError()

    def estimate_difficulty(self, trajectory: Trajectory):
        raise NotImplementedError()
