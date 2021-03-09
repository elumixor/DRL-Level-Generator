from typing import Optional, Union

import numpy as np

from .game_object import GameObject
from ..color import Color
from ..point import Point
from ..renderables import Renderable
from ..shaders import Shader


class Rectangle(GameObject):
    def __init__(self, width_or_size: float,
                 height: Union[float, int, Color] = None,
                 color: Optional[Color] = None,
                 position: Optional[Point] = None,
                 scale: Optional[Point] = None,
                 rotation: float = 0.0,
                 parent: Optional[GameObject] = None):
        if position is None:
            position = Point.zero
        if scale is None:
            scale = Point.one

        hw = width_or_size * 0.5
        if isinstance(height, Color):
            color = height
            hh = hw
        elif isinstance(height, float) or isinstance(height, int):
            hh = height * 0.5
            color = color
        else:
            raise TypeError("Rectangle requires either size or width and height to be specified")

        positions = np.array([
            [-hw, -hh],
            [-hw, hh],
            [hw, hh],
            [hw, -hh],
        ], dtype=np.float32)

        indices = np.array([[0, 2, 1], [0, 3, 2]], dtype=np.uintc)

        renderable = Renderable(positions, indices, color, Shader.unlit)
        super().__init__(position, scale, rotation, parent, renderable)
