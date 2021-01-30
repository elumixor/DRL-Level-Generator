import numpy as np
from OpenGL.GL import *

from .renderable import Renderable
from ..color import Color
from ..shaders import Shader


class CircleRenderable(Renderable):
    def __init__(self, radius: float, color: Color):
        positions = np.array([
            [-radius, -radius],
            [-radius, radius],
            [radius, radius],
            [radius, -radius],
        ], dtype=np.float32)

        indices = np.array([[0, 2, 1], [0, 3, 2]], dtype=np.uintc)

        self._radius_location = None
        self._uv_location = None

        super().__init__(positions, indices, color, Shader.circle)

        uv = np.array([[0, 1],
                       [1, 1],
                       [1, 0],
                       [0, 0]], dtype=np.float32)

        self._uv_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._uv_buffer)
        glBufferData(GL_ARRAY_BUFFER, 4 * uv.size, uv, GL_STATIC_DRAW)

        self.radius = radius

    def render(self, transform_matrix):
        self._shader.use()

        # Set positions
        glEnableVertexAttribArray(self._position_location)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
        glVertexAttribPointer(self._position_location, 2, GL_FLOAT, GL_FALSE, 0, None)

        # Set UV
        glEnableVertexAttribArray(self._uv_location)
        glBindBuffer(GL_ARRAY_BUFFER, self._uv_buffer)
        glVertexAttribPointer(self._uv_location, 2, GL_FLOAT, GL_FALSE, 0, None)

        # Set color
        glUniform4fv(self._color_location, 1, self.color.to_numpy)

        # Set radius
        glUniform1f(self._radius_location, self.radius)

        # Set transform matrix
        glUniformMatrix3fv(self._matrix_location, 1, GL_FALSE, transform_matrix)

        # Pass index array
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._index_buffer)

        # Draw call
        glDrawElements(GL_TRIANGLES, self._indices_length, GL_UNSIGNED_INT, None)

        # Disable VBO after it's no longer needed (to prevent accidental change)
        glDisableVertexAttribArray(self._position_location)

        # Disable UV buffer after it's no longer needed (to prevent accidental change)
        glDisableVertexAttribArray(1)

    def _update_attributes(self):
        super()._update_attributes()

        self._radius_location = self._shader.get_uniform_location("radius")
        self._uv_location = self._shader.get_attribute_location("vertexUV")
