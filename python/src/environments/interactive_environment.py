from typing import Tuple, Any

import glfw
import numpy as np

from rendering import RenderingContext, Triangle, Color, Circle, Point, Rectangle
from .renderable_environment import RenderableEnvironment


class InteractiveEnvironment(RenderableEnvironment):
    @property
    def observation_space(self):
        pass

    @property
    def action_space(self):
        pass

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, Any]:
        pass

    def __init__(self, rendering_context: RenderingContext):
        RenderableEnvironment.__init__(self, rendering_context)

        rendering_context.clear_color = Color(0.9, 0.9, 0.9, 1)

        Triangle(Point.left, Point.up, Point.right, Color.red, scale=Point.one * 0.25, parent=self.game_object)
        Rectangle(1, 1, Color.green, scale=Point.one * 0.5, position=Point.up * 0.5, parent=self.game_object)
        self.circle = Circle(0.5, Color(0.8, 0.1, 0.6, 0.5), parent=self.game_object)

    def reset(self):
        self.circle.transform.local_position = Point.zero

    def apply_action(self):
        rc = self.rendering_context
        if rc.is_key_down(glfw.KEY_ESCAPE):
            return None, None, None, True

        if rc.is_key_down(glfw.KEY_E):
            self.circle.transform.local_scale += Point.one * 0.1
        elif rc.is_key_down(glfw.KEY_Q):
            self.circle.transform.local_scale -= Point.one * 0.1

        if rc.is_key_down(glfw.KEY_W):
            self.circle.transform.local_position.y += 0.1
        elif rc.is_key_down(glfw.KEY_S):
            self.circle.transform.local_position.y -= 0.1

        if rc.is_key_down(glfw.KEY_A):
            self.circle.transform.local_position.x -= 0.1
        elif rc.is_key_down(glfw.KEY_D):
            self.circle.transform.local_position.x += 0.1

        action = 0
        reward = 1

        rc.render_frame()

        next_state = self.circle.transform.local_scale.x

        return action, reward, next_state, False
