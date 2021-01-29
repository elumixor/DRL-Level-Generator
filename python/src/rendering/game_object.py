from __future__ import annotations

from typing import Optional, List

import numpy as np

from .point import Point
from .renderable import Renderable
from .transform import Transform


class GameObject:
    def __init__(self, position=Point.zero, scale=Point.one, parent: Optional[GameObject] = None,
                 renderable: Optional[Renderable] = None):
        self.transform = Transform(position, scale)
        self.children: List[GameObject] = []
        self.renderable = renderable

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

    @property
    def global_matrix(self):
        if self.parent is None:
            return self.transform.local_matrix

        return self.parent.global_matrix @ self.transform.local_matrix

    @property
    def global_center(self):
        return self.global_matrix @ np.array([0, 0, 1], dtype=np.float32)

    def render(self, parent_matrix):
        local_matrix = parent_matrix @ self.transform.local_matrix

        # render self
        if self.renderable is not None:
            self.renderable.render(local_matrix)

        # render children
        for child in self.children:
            child.render(local_matrix)
