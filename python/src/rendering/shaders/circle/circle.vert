#version 410 core

in vec2 position;
in vec2 vertexUV;

uniform mat3 matrix;

out vec2 uv;

void main() {
    vec3 translated = transpose(matrix) * vec3(position.xy, 1);
    gl_Position = vec4(translated.xy, 0, 1);
    uv = vertexUV;
}