import numpy as np

from rendering import Shader, ShaderType, Polygon, Context
from rendering.game_object import GameObject


def main():
    context = Context(800, 600)

    shader = Shader(ShaderType.Unlit)

    t1 = Polygon(np.array([-0.5, -0.5,
                           0.5, -0.5,
                           0.0, 0.5], dtype=np.float32),
                 np.array([0, 1, 2], dtype=np.uintc),
                 np.array([1.0, 0.0, 1.0, 1.0], dtype=np.float32),
                 shader)

    t2 = Polygon(np.array([-0.25, -0.5,
                           0.75, -0.5,
                           0.25, 0.5], dtype=np.float32),
                 np.array([0, 1, 2], dtype=np.uintc),
                 np.array([0.0, 0.0, 1.0, 1.0], dtype=np.float32),
                 shader)

    GameObject(parent=context.main_scene, polygon=t1)
    GameObject(parent=context.main_scene, polygon=t2)

    context.render()


if __name__ == "__main__":
    main()
