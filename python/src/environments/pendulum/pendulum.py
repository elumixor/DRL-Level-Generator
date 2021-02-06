from core.environments import ConfigurableObject
from rendering import GameObject, Rectangle, Color, Point, Circle


class PendulumStaticConfiguration:
    size = 4

    def __init__(self, bob_radius: float, max_angle: float, connector_length: float, vertical_speed: float):
        self.bob_radius = bob_radius
        self.max_angle = max_angle
        self.connector_length = connector_length
        self.vertical_speed = vertical_speed

    def __iter__(self):
        yield self.bob_radius
        yield self.max_angle
        yield self.connector_length
        yield self.vertical_speed


class PendulumDynamicConfiguration:
    size = 3

    def __init__(self, angle: float, position: float, angular_speed: float):
        self.angle = angle
        self.position = position
        self.angular_speed = angular_speed

    def __iter__(self):
        yield self.angle
        yield self.position
        yield self.angular_speed


class Pendulum(ConfigurableObject, GameObject):
    connector_color = Color.greyscale(0.2)
    bob_color = Color.greyscale(0.5)
    line_color = Color.greyscale(0.05)

    def __init__(self, configuration: PendulumStaticConfiguration):
        super().__init__()

        self.line = Rectangle(0.01, 10, Pendulum.line_color)
        self.connector = Rectangle(0.5, 1, Pendulum.connector_color)
        self.attachment = Circle(Pendulum.connector_color)
        self.bob = Circle(Pendulum.bob_color)

        self.add_child(self.line, self.connector, self.attachment, self.bob)

        bob_radius = configuration.bob_radius * 2
        connector_radius = bob_radius * 0.15
        connector_width = connector_radius * 0.5
        connector_height = configuration.connector_length

        self.connector.transform.local_scale = Point(connector_width, connector_height)
        self.connector.transform.local_position = 0.5 * connector_height * Point.down

        self.attachment.transform.local_scale = connector_radius * Point.one

        self.bob.transform.local_scale = bob_radius * Point.one
        self.bob.transform.local_position = connector_height * Point.down

    def update(self, configuration: PendulumDynamicConfiguration):
        self.transform.rotation = configuration.angle
        self.line.transform.rotation = -configuration.angle
        self.transform.local_position = configuration.position * Point.up
