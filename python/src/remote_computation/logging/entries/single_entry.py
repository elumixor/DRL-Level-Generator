from .log_entry import LogEntry


class SingleEntry(LogEntry):

    def __str__(self):
        return f"{self.value}"
