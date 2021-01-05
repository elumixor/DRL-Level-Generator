from .log_entry import LogEntry


class RangedEntry(LogEntry):

    def __init__(self, min_value: float, mean_value: float, max_value: float):
        super(RangedEntry, self).__init__(mean_value)
        self.max_value = max_value
        self.min_value = min_value

    def __str__(self):
        return f"({self.min_value:.2f} {self.value:.2f} {self.max_value:.2f})"

    def __repr__(self):
        return str(self)
