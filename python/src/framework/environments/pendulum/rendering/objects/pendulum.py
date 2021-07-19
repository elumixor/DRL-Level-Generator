from typing import Optional

from rendering import GameObject, Rectangle, Circle, Point, Color

connector_color = Color.greyscale(0.2)
bob_color = Color.greyscale(0.5)
line_color = Color.greyscale(0.05)


class Pendulum(GameObject):
    def __init__(self, bob_radius: float, connector_length: float, parent: Optional[GameObject] = None):
        super().__init__(parent=parent)

        self.line = Rectangle(0.01, 10, line_color)
        self.connector = Rectangle(0.5, 1, connector_color)
        self.attachment = Circle(connector_color)
        self.bob = Circle(bob_color)

        self.add_child(self.line, self.connector, self.attachment, self.bob)

        bob_radius = bob_radius * 2
        connector_radius = bob_radius * 0.15
        connector_width = connector_radius * 0.5

        self.connector.transform.local_scale = Point(connector_width, connector_length)
        self.connector.transform.local_position = 0.5 * connector_length * Point.down

        self.attachment.transform.local_scale = connector_radius * Point.one

        self.bob.transform.local_scale = bob_radius * Point.one
        self.bob.transform.local_position = connector_length * Point.down
