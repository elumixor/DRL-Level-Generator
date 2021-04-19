from __future__ import annotations

import glfw
import numpy as np
from OpenGL.GL import *
from PIL import Image

from utils import log, classproperty
from .color import Color
from .game_objects import GameObject


class RenderingContext:
    def __init__(self, width, height, title=""):
        self.height = height
        self.width = width

        if not glfw.init():
            log.error("glfw.init() failed")
            return

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            log.error("Could not create window")
            glfw.terminate()
            return

        glfw.make_context_current(self.window)

        self._clear_color = Color.black
        glClearColor(0.0, 0.0, 0.0, 1.0)

        # Enable blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Enable backface culling
        glEnable(GL_CULL_FACE)

        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        self._main_scene = GameObject()

        # Constant AR
        aspect = width / height
        self._projection_matrix = np.array([[1, 0, 0], [0, aspect, 0], [0, 0, 1]], dtype=np.float32)

        def resize_callback(window, width, height):
            aspect = width / height
            glViewport(0, 0, width, height)
            self._projection_matrix = np.array([[1, 0, 0], [0, aspect, 0], [0, 0, 1]], dtype=np.float32)

        glfw.set_framebuffer_size_callback(self.window, resize_callback)

        self.keys_down = []

        def on_key_event(window, key, scancode, action, mods):
            if action == glfw.PRESS:
                self.keys_down.append(key)

        glfw.set_key_callback(self.window, on_key_event)

        # Set up rendering to the texture
        self.fb = glGenFramebuffers(1)

    def __del__(self):
        glfw.terminate()

    # noinspection PyMethodParameters
    @classproperty
    def instance(cls) -> RenderingContext:
        try:
            return cls.__static_instance
        except AttributeError:
            instance = RenderingContext(800, 600)
            # noinspection PyAttributeOutsideInit
            cls.__static_instance = instance
            return instance

    @property
    def clear_color(self):
        return self._clear_color

    @clear_color.setter
    def clear_color(self, value: Color):
        self._clear_color = value
        glClearColor(*value.to_numpy)

    @property
    def main_scene(self):
        return self._main_scene

    def render_frame(self):
        self.keys_down = []
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        self._main_scene.render(self._projection_matrix)
        glfw.swap_buffers(self.window)

    def render(self):
        while not glfw.window_should_close(self.window) and not self.is_key_pressed(glfw.KEY_ESCAPE):
            self.render_frame()

        glfw.terminate()

    def renderTexture(self, resolution=2):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fb)

        width = self.width * resolution
        height = self.height * resolution

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, texture, 0)
        glDrawBuffers(1, [GL_COLOR_ATTACHMENT0])

        # Render
        glBindFramebuffer(GL_FRAMEBUFFER, self.fb)
        glViewport(0, 0, width, height)

        glClear(GL_COLOR_BUFFER_BIT)
        self._main_scene.render(self._projection_matrix)

        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (width, height), data).transpose(Image.FLIP_TOP_BOTTOM)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, self.width, self.height)

        return image

    def is_key_pressed(self, key):
        return key in self.keys_down

    def is_key_held(self, key):
        return glfw.get_key(self.window, key) == glfw.PRESS
