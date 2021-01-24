import glfw
import numpy as np
from OpenGL.GL import *

from rendering.game_object import GameObject
from utilities import eprint


class Context:
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
        self.window = glfw.create_window(800, 600, title, None, None)

        if not self.window:
            eprint("Could not create window")
            glfw.terminate()
            return

        glfw.make_context_current(self.window)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        self._main_scene = GameObject()
        self._projection_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)

    @property
    def main_scene(self):
        return self._main_scene

    def render_frame(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self._main_scene.render(self._projection_matrix)
        glfw.swap_buffers(self.window)

    def render(self):
        while not glfw.window_should_close(self.window) and glfw.get_key(self.window, glfw.KEY_ESCAPE) != glfw.PRESS:
            glfw.poll_events()
            self.render_frame()

        glfw.terminate()
