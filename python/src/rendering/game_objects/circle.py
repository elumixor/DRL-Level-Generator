from typing import Optional

from .game_object import GameObject
from ..color import Color
from ..point import Point
from ..renderables import CircleRenderable


class Circle(GameObject):
    def __init__(self, color: Color,
                 radius: float = 0.5,
                 position: Optional[Point] = None,
                 rotation: float = 0.0,
                 parent: Optional[GameObject] = None):
        if position is None:
            position = Point.zero
        scale = radius * Point.one
        circle = CircleRenderable(color, 0.5)
        super().__init__(position, scale, rotation, parent, circle)

    @property
    def radius(self):
        return self.transform.local_scale.x

    @radius.setter
    def radius(self, value):
        self.transform.local_scale.set(value)
