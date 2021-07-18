from typing import Tuple

from torch import Tensor

from .abstract_environment import AbstractEnvironment


class PendulumEnvironment(AbstractEnvironment):
    def __init__(self):
        pass

    def transition(self, state: Tensor, action: Tensor) -> Tuple[Tensor, float, bool]:
        pass
