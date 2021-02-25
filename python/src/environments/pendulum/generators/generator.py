from abc import abstractmethod, ABC

from ..state import PendulumState


class PendulumGenerator(ABC):
    @abstractmethod
    def generate(self, difficulty: float, seed: float) -> PendulumState:
        ...
