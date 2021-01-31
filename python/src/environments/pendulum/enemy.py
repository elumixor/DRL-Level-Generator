from rendering import Point, Color, Circle
from ..configurable_object import ConfigurableObject


class EnemyStaticConfiguration:
    size = 3

    def __init__(self, radius: float, x: float, y: float):
        self.radius = radius
        self.position = Point(x, y)

    def __iter__(self):
        yield self.radius
        yield from self.position


class EnemyDynamicConfiguration:
    size = 0

    def __iter__(self):
        yield from ()


class Enemy(ConfigurableObject, Circle):
    color = Color.red

    def __init__(self, configuration: EnemyStaticConfiguration):
        super().__init__(Enemy.color)
        self.reset(configuration)

    def reset(self, configuration: EnemyStaticConfiguration) -> EnemyDynamicConfiguration:
        radius, x, y = configuration

        self.transform.local_position = Point(x, y)
        self.transform.local_scale = Point.one * radius

        return EnemyDynamicConfiguration()

    def update(self, configuration: EnemyDynamicConfiguration):
        pass
