import numpy as np
from OpenGL.GL import *

from .shaders import Shader


class Renderable:
    def __init__(self, positions: np.ndarray, indices: np.ndarray, color: np.ndarray, shader: Shader):
        self._shader = shader
        self._position_location = None
        self._color_location = None
        self._matrix_location = None
        self._update_attributes()

        # Vertices
        self._vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, 4 * positions.size, positions, GL_STATIC_DRAW)

        # Indices
        self._index_buffer = glGenBuffers(1)
        self._indices_length = indices.size
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._index_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * self._indices_length, indices, GL_STATIC_DRAW)

        self.color = color

    @property
    def shader(self) -> Shader:
        return self._shader

    @shader.setter
    def shader(self, value: Shader):
        self._shader = value
        self._update_attributes()

    def render(self, transform_matrix):
        self._shader.use()

        # Set positions
        glEnableVertexAttribArray(self._position_location)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glVertexAttribPointer(self._position_location, 2, GL_FLOAT, GL_FALSE, 0, None)

        # Set color
        glUniform4fv(self._color_location, 1, self.color)

        # Set transform matrix
        glUniformMatrix3fv(self._matrix_location, 1, GL_FALSE, transform_matrix)

        # Pass index array
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._index_buffer)

        # Draw call
        glDrawElements(GL_TRIANGLES, self._indices_length, GL_UNSIGNED_INT, None)

        # Disable VBO after it's no longer needed (to prevent accidental change)
        glDisableVertexAttribArray(self._position_location)

    def _update_attributes(self):
        self._position_location = self._shader.get_attribute_location("position")
        self._color_location = self._shader.get_uniform_location("color")
        self._matrix_location = self._shader.get_uniform_location("matrix")
