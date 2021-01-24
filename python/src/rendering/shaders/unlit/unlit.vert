#version 410 core
in vec2 position;
uniform mat3 matrix;

void main() {
    gl_Position = vec4(matrix * vec3(position.xy, 1), 1);
}