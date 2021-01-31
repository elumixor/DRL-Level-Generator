from __future__ import annotations

import os
from typing import Dict

import OpenGL.GL.shaders as S
from OpenGL.GL import *

file_path = os.path.realpath(__file__)
base_path = os.path.split(file_path)[0]


class ShaderProperties(type):
    _shader_cache: Dict[str, Shader] = dict()

    @property
    def unlit(cls):
        return cls._try_get("unlit")

    @property
    def circle(cls):
        return cls._try_get("circle")

    def _try_get(cls, shader_name: str):
        if shader_name in cls._shader_cache:
            return cls._shader_cache[shader_name]

        return Shader(shader_name)


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
