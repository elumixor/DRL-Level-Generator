import glfw
import numpy

from OpenGL.GL import *
import OpenGL.GL.shaders

from utilities import eprint


class GLContext:
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

    def start_main_loop(self):
        ...


def create_context(window_width, window_height) -> GLContext:
    return GLContext(window_width, window_height)
