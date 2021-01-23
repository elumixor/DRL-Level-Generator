from enum import Enum


class MessageType(int, Enum):
    ObtainModel = 0
    LoadModel = 1
    SaveModel = 2
    RunTask = 3
    SetLogOptions = 4

    ShowLog = 90

    Test = 99
