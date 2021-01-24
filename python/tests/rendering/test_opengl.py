import glfw
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders

from utilities import eprint


class Triangle:
    def __init__(self, positions, indices, color):
        # todo: pass shader in constructor, change attribute pointers when shader changes

        self.indices_length = len(indices)

        self.positions_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.positions_buffer)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(positions), positions, GL_STATIC_DRAW)

        self.index_buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * self.indices_length, indices, GL_STATIC_DRAW)

        self.color = color

    def render(self, shader, position_name="position", color_name="color"):
        # Set positions
        position = glGetAttribLocation(shader, position_name)
        glEnableVertexAttribArray(position)
        glBindBuffer(GL_ARRAY_BUFFER, self.positions_buffer)
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)

        # Set color
        color = glGetUniformLocation(shader, color_name)
        glUniform4fv(color, 1, self.color)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
        glDrawElements(GL_TRIANGLES, self.indices_length, GL_UNSIGNED_INT, None)

        # Disable VBO
        glDisableVertexAttribArray(position)


def main():
    if not glfw.init():
        eprint("glfw.init() failed")
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(800, 600, "", None, None)

    if not window:
        eprint("Could not create window")
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    vertex_shader = """
    #version 410 core
    in vec4 position;

    void main()
    {
        gl_Position = position;
    }

    """

    fragment_shader = """
    #version 410 core
    uniform vec4 color;
    out vec4 frag_color;

    void main()
    {
        frag_color = color;
    }
    """

    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    t1 = Triangle(np.array([-0.5, -0.5, 0.0,
                            0.5, -0.5, 0.0,
                            0.0, 0.5, 0.0], dtype=np.float32),
                  np.array([0, 1, 2], dtype=np.uintc),
                  np.array([1.0, 0.0, 1.0, 1.0], dtype=np.float32))

    t2 = Triangle(np.array([-0.25, -0.5, 0.0,
                            0.75, -0.5, 0.0,
                            0.25, 0.5, 0.0], dtype=np.float32),
                  np.array([0, 1, 2], dtype=np.uintc),
                  np.array([0.0, 0.0, 1.0, 1.0], dtype=np.float32))

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        # Objets needs a VBO

        # Draw triangle (each draw call)
        glUseProgram(shader)
        t1.render(shader)
        t2.render(shader)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
