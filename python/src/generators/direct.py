from typing import Literal, Optional

from torch.nn import Module, Linear, Identity

from common import Remap, Clamp


class DirectGenerator(Module):
    """
    Outputs the x position directly
    """

    def __init__(self, x_min, x_max, constrain: Optional[Literal["clamp", "remap"]] = None):
        super().__init__()
        self.l1 = Linear(1, 4)
        self.l2 = Linear(4, 4)
        self.l3 = Linear(4, 1)

        if constrain == "remap":
            self.constrain = Remap(x_min, x_max)
        elif constrain == "clamp":
            self.constrain = Clamp(x_min, x_max)
        else:
            self.constrain = Identity()

    def forward(self, x):
        x = self.l1(x).relu()
        x = self.l2(x).relu()
        unconstrained_x = self.l3(x)
        constrained_x = self.constrain(unconstrained_x)
        return constrained_x, unconstrained_x
