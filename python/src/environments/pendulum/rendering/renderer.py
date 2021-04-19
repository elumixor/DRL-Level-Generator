from typing import Optional

from rendering import RenderingContext, GameObject, Color
from utils import vec
from .enemy import Enemy
from .pendulum import Pendulum
from ...renderer import Renderer, TState


class PendulumRenderer(Renderer[vec]):
    def render_state(self, state: TState):
        if not self.pendulum:
            self.pendulum = Pendulum(state)
            self.enemy = Enemy(state)
            self.game_object.add_child(self.pendulum, self.enemy)
        else:
            self.pendulum.update(state)
            self.enemy.update(state)

        self.context.render_frame()

    def __init__(self):
        self.context = RenderingContext.instance

        # Set a pleasant background color
        self.context.clear_color = Color.greyscale(0.9)

        self.game_object = GameObject(parent=self.context.main_scene)

        # Pendulum game object
        self.pendulum: Optional[Pendulum] = None

        # Enemy game object
        self.enemy: Optional[Enemy] = None
