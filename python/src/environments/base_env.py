from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Optional, Callable, Tuple

from .renderer import Renderer
from .spaces import Space

TState = TypeVar("TState")
TAction = TypeVar("TAction")

TStateSpace = TypeVar("TStateSpace", bound=Space)
TActionSpace = TypeVar("TActionSpace", bound=Space)


class EnvInstance(Generic[TState, TAction]):
    def __init__(self, env: BaseEnv[TState, TAction]):
        self.env = env
        self.state = env.state_space.sample()

    def reset(self):
        self.state = self.env.state_space.sample()

    def step(self, action: TAction) -> TState:
        self.state = self.env.transition(self.state, action)
        return self.state

    def render(self, state: TState):
        self.env.render(state)


TEnvInstance = TypeVar("TEnvInstance", bound=EnvInstance)


class BaseEnv(ABC, Generic[TState, TAction]):
    def __init__(self,
                 renderer_class: Callable[[], Renderer[TState]],
                 instance_class: Optional[Callable[[BaseEnv], TEnvInstance]] = None):
        if not instance_class:
            instance_class = EnvInstance

        self.renderer: Optional[Renderer[TState]] = None

        self.renderer_class = renderer_class
        self.instance_class = instance_class

    def __call__(self) -> EnvInstance[TState, TAction]:
        return self.instantiate()

    @property
    @abstractmethod
    def state_space(self) -> Space:
        ...

    @property
    @abstractmethod
    def action_space(self) -> Space:
        ...

    @abstractmethod
    def transition(self, state: TState, action: TAction) -> Tuple[TState, float, bool]:
        ...

    def instantiate(self) -> TEnvInstance:
        return self.instance_class(self)

    def render(self, state: TState):
        if not self.renderer:
            self.renderer = self.renderer_class()

        self.renderer.render_state(state)
