from abc import ABC, abstractmethod


class LogEntry(ABC):

    def __init__(self, value: float):
        self.value = value

    @abstractmethod
    def __str__(self):
        pass
