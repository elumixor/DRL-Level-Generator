from .log_entry import LogEntry


class RangedEntry(LogEntry):

    def __init__(self, min_value: float, mean_value: float, max_value: float):
        self.max_value = max_value
        self.mean_value = mean_value
        self.min_value = min_value

    def __str__(self):
        return f"{self.min_value} {self.mean_value} {self.max_value}"
