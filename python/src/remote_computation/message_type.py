from enum import Enum


class MessageType(int, Enum):
    ObtainModel = 0
    LoadModel = 1
    SaveModel = 2
    RunTask = 3

    Test = 99
