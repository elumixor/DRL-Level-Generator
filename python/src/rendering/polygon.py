from collections import Iterable

from rendering.point import Point
from rendering.transform import Transform


class Polygon:
    def __init__(self, transform: Transform, points: Iterable[Point]):
        self.transform = transform
        self._points = points

    @property
    def local_points(self):
        return self._points[:]

    @property
    def global_points(self):
        matrix = self.transform.global_matrix
        return [point.get_global(matrix) for point in self._points]
