import numpy as np

from rendering import GameObject, Rectangle, Color, Point, Circle
from ..state import bob_radius, connector_length, current_angle, position


class Pendulum(GameObject):
    connector_color = Color.greyscale(0.2)
    bob_color = Color.greyscale(0.5)
    line_color = Color.greyscale(0.05)

    def __init__(self, state: np.ndarray):
        super().__init__()

        self.line = Rectangle(0.01, 10, Pendulum.line_color)
        self.connector = Rectangle(0.5, 1, Pendulum.connector_color)
        self.attachment = Circle(Pendulum.connector_color)
        self.bob = Circle(Pendulum.bob_color)

        self.add_child(self.line, self.connector, self.attachment, self.bob)

        _bob_radius = state[bob_radius] * 2
        connector_radius = _bob_radius * 0.15
        connector_width = connector_radius * 0.5
        connector_height = state[connector_length]

        self.connector.transform.local_scale = Point(connector_width, connector_height)
        self.connector.transform.local_position = 0.5 * connector_height * Point.down

        self.attachment.transform.local_scale = connector_radius * Point.one

        self.bob.transform.local_scale = _bob_radius * Point.one
        self.bob.transform.local_position = connector_height * Point.down

    def update(self, state: np.ndarray):
        self.transform.rotation = state[current_angle]
        self.line.transform.rotation = -state[current_angle]
        self.transform.local_position = state[position] * Point.up
