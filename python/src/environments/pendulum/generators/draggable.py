import glfw
import numpy as np

from rendering import RenderingContext, Circle, Color, Point
from utilities import clamp
from .generator import PendulumGenerator
from ..state import PendulumState


class DraggableGenerator(PendulumGenerator):
    def __init__(self, ctx: RenderingContext, speed=0.01, fast_speed=0.1, min_x=-0.5, max_x=0.5,
                 min_y=-0.25, max_y=0.75, bob_radius=0.15, max_angle=np.deg2rad(30), angle=np.deg2rad(30),
                 angular_speed=np.deg2rad(5), vertical_speed=0.02, connector_length=0.5):
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

        self.bob_radius = bob_radius
        self.max_angle = max_angle
        self.connector_length = connector_length
        self.vertical_speed = vertical_speed
        self.angle = angle
        self.angular_speed = angular_speed

        self.hint = Circle(Color(1, 0, 0, 0.3), position=Point(self.enemy_x, self.enemy_y),
                           scale=Point.one * 2 * self.enemy_radius, parent=ctx.main_scene)

    def generate(self, difficulty: float, seed: float) -> PendulumState:
        position = 0

        return PendulumState(self.bob_radius, self.max_angle, self.connector_length, self.vertical_speed,
                             self.enemy_x, self.enemy_y, self.enemy_radius,
                             self.angle, position, self.angular_speed)

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

    @property
    def config(self):
        return {
            "Enemy x": self.enemy_x,
            "Enemy y": self.enemy_y,
            "Enemy radius": self.enemy_radius,
            "Bob radius": self.bob_radius,
            "Max angle": self.max_angle,
            "Connector length": self.connector_length,
            "Vertical speed": self.vertical_speed,
            "angle": self.angle,
            "Angular speed": self.angular_speed,
        }
