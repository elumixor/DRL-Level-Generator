from typing import Optional

from rendering import RenderingContext, GameObject, Color, Circle, Point
from utils import vec
from .enemy import Enemy
from .pendulum import Pendulum
from ..state import enemy_radius as s_enemy_radius, size_fixed, position as s_position
from ...renderer import Renderer, TState


class PendulumRenderer(Renderer[vec]):
    def render_state(self, state: TState, to_image=False, **kwargs):
        if not self.pendulum:
            self.pendulum = Pendulum(state)
            self.enemy = Enemy(state)
            self.game_object.add_child(self.pendulum, self.enemy)
        else:
            self.pendulum.update(state)
            self.enemy.update(state)

        dx, _ = self.context.camera_position
        self.context.camera_position = (dx, state[s_position])

        if to_image:
            return self.context.render_texture(resolution=kwargs.get("resolution", 1))

        self.context.render_frame()

    def __init__(self):
        self.context: RenderingContext = RenderingContext.instance

        # Set a pleasant background color
        self.context.clear_color = Color.greyscale(0.9)

        self.game_object = GameObject(parent=self.context.main_scene)

        # Pendulum game object
        self.pendulum: Optional[Pendulum] = None

        # Enemy game object
        self.enemy: Optional[Enemy] = None


class VariablePendulumRenderer(Renderer[vec]):
    def render_state(self, state: TState, to_image=False, **kwargs):
        pendulum = Pendulum(state)

        enemy_radius = state[s_enemy_radius]
        enemies = state[size_fixed:]

        enemies_objects = []

        for i in range(len(enemies) // 2):
            x, y = enemies[2 * i], enemies[2 * i + 1]

            enemy = Circle(Color.red)
            enemy.transform.local_position = Point(x, y)
            enemy.transform.local_scale = Point.one * enemy_radius * 2

            enemies_objects.append(enemy)

        dx, _ = self.context.camera_position
        self.context.camera_position = (dx, state[s_position])

        self.game_object.children = [pendulum, *enemies_objects]

        if to_image:
            return self.context.render_texture(resolution=kwargs.get("resolution", 1))

        self.context.render_frame()

    def __init__(self):
        self.context: RenderingContext = RenderingContext.instance

        # Set a pleasant background color
        self.context.clear_color = Color.greyscale(0.9)

        self.game_object = GameObject(parent=self.context.main_scene)


def render_variable(ctx, state, resolution=1.0):
    ctx.clear_color = Color.greyscale(0.9)

    game_object = GameObject(parent=ctx.main_scene)

    pendulum = Pendulum(state)

    enemy_radius = state[s_enemy_radius]
    enemies = state[size_fixed:]

    game_object.add_child(pendulum)

    for i in range(len(enemies) // 2):
        x, y = enemies[2 * i], enemies[2 * i + 1]

        enemy = Circle(Color.red)
        enemy.transform.local_position = Point(x, y)
        enemy.transform.local_scale = Point.one * enemy_radius * 2

        game_object.add_child(enemy)

    return ctx.render_texture(resolution=resolution)
