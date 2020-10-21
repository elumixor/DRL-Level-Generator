from enum import Enum


class LayerName(str, Enum):
    Linear = "Linear"
    ReLU = "ReLU"
    Softmax = "Softmax"
    Sequential = "Sequential"
    Identity = "Identity"


class IntParameter(str, Enum):
    InputSize = "InputSize"
    OutputSize = "OutputSize"


class FloatParameter(str, Enum):
    pass
