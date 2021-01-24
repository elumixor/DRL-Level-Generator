#version 410 core

in vec2 position;
in vec2 vertexUV;

uniform mat3 matrix;

out vec2 uv;

void main() {
    gl_Position = vec4(matrix * vec3(position.xy, 1), 1);
    uv = vertexUV;
}