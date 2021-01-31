import numpy as np

from rendering import Shader, RenderingContext, Color
from rendering.game_objects.game_object import GameObject
from rendering.renderables import Renderable, CircleRenderable


def main():
    context = RenderingContext(800, 600)

    shader = Shader.unlit

    t1 = Renderable(np.array([-0.5, -0.5,
                              0.5, -0.5,
                              0.0, 0.5], dtype=np.float32),
                    np.array([0, 1, 2], dtype=np.uintc),
                    Color(1.0, 0.0, 1.0),
                    shader)

    t2 = Renderable(np.array([-0.25, -0.5,
                              0.75, -0.5,
                              0.25, 0.5], dtype=np.float32),
                    np.array([0, 1, 2], dtype=np.uintc),
                    Color.blue,
                    shader)

    t3 = CircleRenderable(Color.green)

    GameObject(parent=context.main_scene, renderable=t1)
    GameObject(parent=context.main_scene, renderable=t2)
    GameObject(parent=context.main_scene, renderable=t3)

    context.render()


if __name__ == "__main__":
    main()
