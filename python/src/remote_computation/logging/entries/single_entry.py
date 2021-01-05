from .log_entry import LogEntry


class SingleEntry(LogEntry):

    def __str__(self):
        return f"{self.value:.2f}"

    def __repr__(self):
        return str(self)
