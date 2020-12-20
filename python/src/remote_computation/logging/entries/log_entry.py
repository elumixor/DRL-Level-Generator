from abc import ABC, abstractmethod


class LogEntry(ABC):

    @abstractmethod
    def __str__(self):
        pass
