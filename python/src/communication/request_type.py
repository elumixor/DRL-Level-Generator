from enum import Enum


class RequestType(str, Enum):
    Echo = "Echo",
    Inference = "Inference",
    Update = "Update",
