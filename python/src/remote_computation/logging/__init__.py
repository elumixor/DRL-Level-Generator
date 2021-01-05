import multiprocessing as mp
import threading
from typing import Dict, Optional

from ._logger import Logger as _Logger
from .entries import LogEntry, SingleEntry, RangedEntry
from .exceptions import LoggingError
from .log_data import LogData
from .log_option import LogOption
from .log_option_name import LogOptionName
from .log_options import LogOptions

_signal_register = 0
_signal_show = 1
_signal_update = 2


def _logger_main(queue: mp.Queue):
    """
    Wrapper around Logger to be used in multiprocessing environment
    where matplotlib.pyplot is shared between loggers
    This thus also allows to display multiple plots simultaneously
    """

    import matplotlib.pyplot as plt
    plt.ion()

    loggers: Dict[int, _Logger] = dict()

    for item in iter(queue.get, None):
        signal = item[0]

        if signal == _signal_register:
            model_id = item[1]
            if model_id in loggers:
                raise RuntimeError(f"Model {model_id} is already registered in the logger")

            options: LogOptions = item[2]

            loggers[model_id] = _Logger(plt, model_id, options)

        elif signal == _signal_show:
            model_id = item[1]
            if model_id not in loggers:
                raise RuntimeError(f"Model {model_id} is not registered in the logger")

            data: LogData = item[2]

            loggers[model_id].show(data)

        elif signal == _signal_update:
            model_id = item[1]
            if model_id not in loggers:
                raise RuntimeError(f"Model {model_id} is not registered in the logger")

            data: LogData = item[2]

            loggers[model_id].update(data)

        else:
            raise RuntimeError(f"Unknown logger signal: {signal}")

    print("Logger end")


class _LoggerWrapper:
    def __init__(self):
        # Start the actual process
        self.queue = mp.Queue(1)
        self.logger_process = mp.Process(target=_logger_main, args=(self.queue,))
        self.logger_process.start()


_wrapper: Optional[_LoggerWrapper] = None


def register(model_id: int, options: LogOptions):
    global _wrapper
    if _wrapper is None:
        _wrapper = _LoggerWrapper()

    _wrapper.queue.put((_signal_register, model_id, options))


def show(model_id: int, data: LogData):
    """Renders current logging data to the plot. Does not update internal state"""
    global _wrapper
    if _wrapper is None:
        _wrapper = _LoggerWrapper()

    _wrapper.queue.put((_signal_show, model_id, data))


def update(model_id: int, data: LogData):
    """Same as show, but also updates internal state of the logger (epochs)"""
    global _wrapper
    if _wrapper is None:
        _wrapper = _LoggerWrapper()

    _wrapper.queue.put((_signal_update, model_id, data))
