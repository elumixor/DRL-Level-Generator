from abc import abstractmethod
from typing import Generic, TypeVar

from environments.spaces import Space

TState = TypeVar("TState")
TAction = TypeVar("TAction")
TStateSpace = TypeVar("TStateSpace", bound=Space)
TActionSpace = TypeVar("TActionSpace", bound=Space)


class Renderer(Generic[TState]):
    @abstractmethod
    def render_state(self, state: TState, to_image=False, **kwargs): ...
