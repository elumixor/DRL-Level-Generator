from enum import Enum

import OpenGL.GL.shaders as S
from OpenGL.GL import *

import sys, os
file_path = os.path.realpath(__file__)
pathname = file_path[:file_path.rindex("/")]

class ShaderType(str, Enum):
    Unlit = "unlit"
    Circle = "circle"


class Shader:
    _base = f"{pathname}"

    def __init__(self, shader_type: ShaderType):
        vertex_path = f"{Shader._base}/{shader_type}/{shader_type}.vert"
        fragment_path = f"{Shader._base}/{shader_type}/{shader_type}.frag"

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
