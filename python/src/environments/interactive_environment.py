from typing import Tuple, Any

import numpy as np
import glfw

from rendering import RenderingContext, Circle, GameObject, Shader, ShaderType, Polygon
from rendering.point import Point
from .gl_renderable import GLRenderable


class InteractiveEnvironment(GLRenderable):
    @property
    def observation_space(self):
        pass

    @property
    def action_space(self):
        pass

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, Any]:
        pass

    def __init__(self, rendering_context: RenderingContext):
        GLRenderable.__init__(self, rendering_context)

        circle = Circle(0.5, np.array([1, 0, 0, 0]))
        self.circle = GameObject(polygon=circle, parent=self.game_object)

    def reset(self):
        self.circle.transform.local_position = Point.zero

    def apply_action(self):
        rc = self.rendering_context
        if rc.is_key_down(glfw.KEY_ESCAPE):
            return None, None, None, True

        if rc.is_key_down(glfw.KEY_E):
            self.circle.transform.local_scale += Point.one
        elif rc.is_key_down(glfw.KEY_Q):
            self.circle.transform.local_scale -= Point.one
        elif rc.is_key_down(glfw.KEY_A):
            self.circle.transform.local_position.x -= 0.1
        elif rc.is_key_down(glfw.KEY_D):
            self.circle.transform.local_position.x += 0.1

        action = 0
        reward = 1

        rc.render_frame()

        next_state = self.circle.transform.local_scale.x

        return action, reward, next_state, False
