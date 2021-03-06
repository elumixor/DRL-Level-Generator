from typing import Optional

from .game_object import GameObject
from ..color import Color
from ..point import Point
from ..renderables import CircleRenderable


class Circle(GameObject):
    def __init__(self, color: Color,
                 radius: float = 0.5,
                 position: Point = Point.zero, scale: Point = Point.one, rotation: float = 0.0,
                 parent: Optional[GameObject] = None):
        circle = CircleRenderable(color, radius)
        super().__init__(position, scale, rotation, parent, circle)
