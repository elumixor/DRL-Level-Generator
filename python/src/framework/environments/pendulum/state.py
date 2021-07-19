from torch import Tensor


class PendulumState(Tensor):
    @classmethod
    def create(cls, current_angle: float, angular_speed: float, vertical_position: float, *enemies_x: float):
        return PendulumState([current_angle, angular_speed, vertical_position, *enemies_x])

    def get_enemy_x(self, enemy_index: int):
        return self[3 + enemy_index]

    def set_enemy_x(self, enemy_index: int, value: float):
        self[3 + enemy_index] = value

    @property
    def current_angle(self):
        return self[0]

    @current_angle.setter
    def current_angle(self, value):
        self[0] = value

    @property
    def angular_speed(self):
        return self[1]

    @angular_speed.setter
    def angular_speed(self, value):
        self[1] = value

    @property
    def vertical_position(self):
        return self[2]

    @vertical_position.setter
    def vertical_position(self, value):
        self[2] = value
