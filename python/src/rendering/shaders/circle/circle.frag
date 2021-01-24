#version 410 core

in vec2 uv;

uniform vec4 color;
uniform float radius;

out vec4 frag_color;

void main() {
    float value = step(length(abs(uv - vec2(0.5, 0.5))), radius);
    frag_color = color * value;
}