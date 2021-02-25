import glfw
import numpy as np

from rendering import RenderingContext, Circle, Color, Point
from utilities import clamp
from .generator import PendulumGenerator
from ..state import PendulumState


class DraggableGenerator(PendulumGenerator):
    def __init__(self, ctx: RenderingContext, speed=0.01, fast_speed=0.1, min_x=-0.5, max_x=0.5,
                 min_y=-0.25, max_y=0.75):
        self.ctx = ctx

        self.speed = speed
        self.fast_speed = fast_speed
        self.min_x = min_x
        self.max_x = max_x

        self.min_y = min_y
        self.max_y = max_y

        self.enemy_radius = 0.1
        self.enemy_y = 0.25
        self.enemy_x = (max_x + min_x) / 2

        self.hint = Circle(Color(1, 0, 0, 0.3), position=Point(self.enemy_x, self.enemy_y),
                           scale=Point.one * 2 * self.enemy_radius, parent=ctx.main_scene)

    def generate(self, difficulty: float, seed: float) -> PendulumState:
        bob_radius = 0.15
        max_angle = np.deg2rad(30)
        connector_length = 0.5
        vertical_speed = 0.02

        enemy_radius = self.enemy_radius
        enemy_x = self.enemy_x
        enemy_y = self.enemy_y

        angle = np.deg2rad(30)
        position = 0
        angular_speed = np.deg2rad(5)

        return PendulumState(bob_radius, max_angle, connector_length, vertical_speed,
                             enemy_x, enemy_y, enemy_radius,
                             angle, position, angular_speed)

    def handle_input(self):
        shift = self.ctx.is_key_held(glfw.KEY_LEFT_SHIFT) or self.ctx.is_key_held(glfw.KEY_RIGHT_SHIFT)

        distance = self.fast_speed if shift else self.speed

        if self.ctx.is_key_held(glfw.KEY_LEFT):
            self.enemy_x -= distance

        elif self.ctx.is_key_held(glfw.KEY_RIGHT):
            self.enemy_x += distance

        if self.ctx.is_key_held(glfw.KEY_UP):
            self.enemy_y += distance

        elif self.ctx.is_key_held(glfw.KEY_DOWN):
            self.enemy_y -= distance

        self.enemy_x = clamp(self.enemy_x, self.min_x, self.max_x)
        self.enemy_y = clamp(self.enemy_y, self.min_y, self.max_y)

        self.hint.transform.local_position = Point(self.enemy_x, self.enemy_y)
