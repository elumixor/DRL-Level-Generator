import glfw
import numpy as np
from OpenGL.GL import *

from rendering.game_objects.game_object import GameObject
from utilities import eprint


class RenderingContext:
    def __init__(self, width, height, title=""):
        self.height = height
        self.width = width

        if not glfw.init():
            eprint("glfw.init() failed")
            return

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            eprint("Could not create window")
            glfw.terminate()
            return

        glfw.make_context_current(self.window)

        self._clear_color = [0.0, 0.0, 0.0, 1.0]

        glClearColor(0.0, 0.0, 0.0, 1.0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        self._main_scene = GameObject()

        aspect = width / height

        self._projection_matrix = np.array([[1, 0, 0], [0, aspect, 0], [0, 0, 1]], dtype=np.float32)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        glfw.terminate()

    @property
    def clear_color(self):
        return self._clear_color

    @clear_color.setter
    def clear_color(self, value):
        self._clear_color = value
        glClearColor(*value)

    @property
    def main_scene(self):
        return self._main_scene

    def render_frame(self):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        self._main_scene.render(self._projection_matrix)
        glfw.swap_buffers(self.window)

    def render(self):
        while not glfw.window_should_close(self.window) and not self.is_key_down(glfw.KEY_ESCAPE):
            self.render_frame()

        glfw.terminate()

    def is_key_down(self, key):
        return glfw.get_key(self.window, key) == glfw.PRESS
