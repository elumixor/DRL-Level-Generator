from enum import Enum


class RequestType(str, Enum):
    Echo = "Echo"
    WakeUp = "WakeUp"
    SendConfiguration = "SendConfiguration"
    SendTrainingData = "SendTrainingData"
    ShutDown = "ShutDown"
    RequestInfo = "RequestInfo"
    SaveSession = "SaveSession"
    LoadSession = "LoadSession"
