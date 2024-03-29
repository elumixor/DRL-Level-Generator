from typing import Optional

import numpy as np

from .game_object import GameObject
from ..color import Color
from ..point import Point
from ..renderables import Renderable
from ..shaders import Shader


class Triangle(GameObject):
    def __init__(self, p1: Point, p2: Point, p3: Point, color: Color,
                 position: Optional[Point] = None,
                 scale: Optional[Point] = None,
                 rotation: float = 0.0,
                 parent: Optional[GameObject] = None):
        if position is None:
            position = Point.zero
        if scale is None:
            scale = Point.one

        positions = np.array([
            [p1.x, p1.y],
            [p2.x, p2.y],
            [p3.x, p3.y],
        ], dtype=np.float32)

        indices = np.array([0, 1, 2], dtype=np.uintc)

        renderable = Renderable(positions, indices, color, Shader.unlit)
        super().__init__(position, scale, rotation, parent, renderable)
