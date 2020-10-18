from enum import Enum


class ResponseType(str, Enum):
    Failure = "Failure"
    Ok = "Ok"
