from framework import State


class PendulumState(State):
    @classmethod
    def create(cls, current_angle: float, angular_speed: float, vertical_position: float, *enemies_x: float):
        return PendulumState([current_angle, angular_speed, vertical_position, *enemies_x])

    @classmethod
    def get_size(cls, num_enemies: int = 1):
        return 3 + num_enemies

    @property
    def embedding(self):
        return self.enemy_x

    @embedding.setter
    def embedding(self, value):
        self.enemy_x = value

    @property
    def current_angle(self):
        return self[..., 0]

    @current_angle.setter
    def current_angle(self, value):
        self[..., 0] = value

    @property
    def angular_speed(self):
        return self[..., 1]

    @angular_speed.setter
    def angular_speed(self, value):
        self[..., 1] = value

    @property
    def vertical_position(self):
        return self[..., 2]

    @vertical_position.setter
    def vertical_position(self, value):
        self[..., 2] = value

    @property
    def enemy_x(self):
        return self[..., 3:]

    @enemy_x.setter
    def enemy_x(self, value):
        self[..., 3:] = value

    def __iter__(self):
        if self.ndim > 1:
            for state in super().__iter__():
                yield PendulumState(state)
        else:
            for component in super().__iter__():
                yield component

    def to_string(self):
        if self.ndim == 1:
            return f"PendulumState(\n  " \
                   f"angle: {self.current_angle:.2f},\n  " \
                   f"angular_speed: {self.angular_speed:.2f},\n  " \
                   f"vertical_position: {self.vertical_position:.2f},\n  " \
                   f"enemies: {', '.join([f'{x:.2f}' for x in self.enemy_x])}\n" \
                   ")"

        return super().__str__()
