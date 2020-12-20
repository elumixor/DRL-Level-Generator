from .log_entry import LogEntry


class SingleEntry(LogEntry):

    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f"{self.value}"
