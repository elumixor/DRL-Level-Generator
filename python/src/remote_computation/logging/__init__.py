from .log_data import LogData
from .log_option import LogOption
from .log_option_name import LogOptionName
from .log_options import LogOptions


def show(data: LogData, options: LogOptions):
    for name, option in options.items():
        option: LogOption

        if name not in data:
            continue

        entry = data[name]

        last = entry[-1]

        if option.print:
            print(str(last))
