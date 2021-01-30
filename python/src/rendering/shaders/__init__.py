import OpenGL.GL.shaders as S
from OpenGL.GL import *

import os

file_path = os.path.realpath(__file__)
base_path = file_path[:file_path.rindex("/")]


class ShaderProperties(type):
    def __getattr__(self, item: str):
        return Shader(item)


class Shader(metaclass=ShaderProperties):
    def __init__(self, shader_name: str):
        vertex_path = f"{base_path}/{shader_name}/{shader_name}.vert"
        fragment_path = f"{base_path}/{shader_name}/{shader_name}.frag"

        with open(vertex_path, "r") as file:
            vertex = file.read()

        with open(fragment_path, "r") as file:
            fragment = file.read()

        self._shader = S.compileProgram(S.compileShader(vertex, GL_VERTEX_SHADER),
                                        S.compileShader(fragment, GL_FRAGMENT_SHADER))

    def use(self):
        glUseProgram(self._shader)

    def get_attribute_location(self, attribute_name: str):
        return glGetAttribLocation(self._shader, attribute_name)

    def get_uniform_location(self, uniform_name: str):
        return glGetUniformLocation(self._shader, uniform_name)
