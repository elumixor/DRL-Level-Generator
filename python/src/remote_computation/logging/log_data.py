from typing import Union, Dict, Tuple, List

from .entries import RangedEntry, SingleEntry, LogEntry
from .entry_type import EntryType
from .log_option_name import LogOptionName


class LogData:

    def __init__(self):
        self.entries: Dict[LogOptionName, List[LogEntry]] = dict()
        self.entries_types: Dict[LogOptionName, EntryType] = dict()

    def add_entry(self, name: LogOptionName, value: Union[float, Tuple[float, float, float]]):
        value_type = EntryType.Ranged if isinstance(value, RangedEntry) else EntryType.Single

        if name not in self.entries_types:
            self.entries_types[name] = value_type
        elif value_type != self.entries_types[name]:
            raise RuntimeError(f"Previous entry type was {self.entries_types[name]}, now is {value_type}")

        entry = RangedEntry(*value) if isinstance(value, Tuple) else SingleEntry(value)
        if name not in self.entries:
            self.entries[name] = [entry]
        else:
            self.entries[name].append(entry)

    def __contains__(self, item: LogOptionName):
        return item in self.entries

    def __getitem__(self, item: LogOptionName) -> List[LogEntry]:
        return self.entries[item]

    def __str__(self):
        s = f"LogData {len(self.entries)} entries:\n"

        for name, data in self.entries.items():
            s += f"\t{name} {data}\n"

        return s

    def __repr__(self):
        return str(self)
