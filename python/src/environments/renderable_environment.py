import torch

from rendering import RenderingContext, GameObject
from .base_environment import BaseEnvironment
from abc import ABC, abstractmethod


class RenderableEnvironment(BaseEnvironment, ABC):
    def __init__(self, rendering_context: RenderingContext):
        self.rendering_context = rendering_context
        self.game_object = GameObject(parent=rendering_context.main_scene)

        BaseEnvironment.__init__(self)

    def render(self):
        self.rendering_context.render_frame()

    @abstractmethod
    def set_state(self, state: torch.tensor):
        ...
