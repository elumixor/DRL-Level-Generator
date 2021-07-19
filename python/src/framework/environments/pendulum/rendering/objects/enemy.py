from typing import Optional

from rendering import Circle, Color, Point, GameObject


class Enemy(Circle):
    def __init__(self, x: float, y: float, radius: float, parent: Optional[GameObject] = None):
        super().__init__(Color.red, parent=parent)

        self.x = x
        self.y = y

        self.transform.local_scale = Point.one * radius * 2
