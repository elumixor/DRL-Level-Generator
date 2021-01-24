from __future__ import annotations

from typing import Optional, List

from .point import Point
from .polygon import Polygon
from .transform import Transform


class GameObject:
    # Todo: add collider
    def __init__(self, position=Point.zero, scale=Point.one, parent: Optional[GameObject] = None,
                 polygon: Optional[Polygon] = None):
        self.transform = Transform(position, scale)
        self.children: List[GameObject] = []
        self.polygon = polygon

        self._parent = None
        if parent is not None:
            self.parent = parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if self._parent is not None:
            self._parent.children.remove(self)

        self._parent = value
        self._parent.children.append(self)

    def render(self, parent_matrix):
        local_matrix = parent_matrix @ self.transform.local_matrix

        # render self
        if self.polygon is not None:
            self.polygon.render(local_matrix)

        # render children
        for child in self.children:
            child.render(local_matrix)
