from typing import Optional, List

from framework import LazyRenderer
from rendering import RenderingContext, GameObject, Color
from .objects import Enemy, Pendulum
from ..state import PendulumState


class PendulumRenderer(LazyRenderer):
    def __init__(self, bob_radius: float, connector_length: float, enemy_radius: float, *enemies_y: float):
        super().__init__()

        self.bob_radius = bob_radius
        self.connector_length = connector_length
        self.enemy_radius = enemy_radius
        self.enemies_y = enemies_y

        self.num_enemies = len(enemies_y)

        self.scene: Optional[GameObject] = None
        self.pendulum: Optional[Pendulum] = None
        self.enemies: Optional[List[Enemy]] = None
        self.rendering_context: Optional[RenderingContext] = None

    def render(self, state: PendulumState, to_image=False, resolution=1, width=None, height=None):
        super().render(state)

        current_angle, _, vertical_position, *enemies_x = state

        self.pendulum.angle = current_angle
        self.pendulum.y = vertical_position

        for enemy, x in zip(self.enemies, enemies_x):
            enemy.x = x

        # Adjust camera position so that the pendulum is in the center
        dx, _ = self.rendering_context.camera_position
        self.rendering_context.camera_position = dx, vertical_position

        if to_image:
            return self.rendering_context.render_texture(resolution=resolution, width=width, height=height)

        # Render the scene
        self.rendering_context.render_frame()

    def lazy_init(self, state: PendulumState):
        # Get a rendering context
        self.rendering_context: RenderingContext = RenderingContext.instance

        # Clear all children from it
        self.rendering_context.main_scene.remove_children()

        # Set a pleasant color
        self.rendering_context.clear_color = Color.greyscale(0.9)

        # Create our own scene
        self.scene = GameObject(parent=self.rendering_context.main_scene)

        # Create a pendulum
        self.pendulum = Pendulum(self.bob_radius, self.connector_length, parent=self.scene)

        # Create enemies
        enemies_x = state.enemy_x
        self.enemies = [Enemy(x, y, self.enemy_radius, parent=self.scene) for x, y in zip(enemies_x, self.enemies_y)]
