from typing import List, Optional

from .logger import Logger


def auto_logged(print_names: Optional[List[str]] = None, plot_names: Optional[List[str]] = None,
                capacity=100, plot_columns=3):
    if plot_names is None:
        plot_names = []
    if print_names is None:
        print_names = []

    all_names = list(dict.fromkeys(plot_names + print_names))

    class C:
        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):
            instance = self.func(*args, **kwargs)
            logger = Logger(print_names, plot_names, capacity, plot_columns)

            def print_progress():
                logger.print()

            def plot_progress():
                logger.plot()

            instance.print_progress = print_progress
            instance.plot_progress = plot_progress
            previous = instance.update

            def update(*args, **kwargs):
                previous(*args, **kwargs)

                logger.update(**{
                    attribute: float(getattr(instance, attribute)) for attribute in all_names
                })

            instance.update = update

            return instance

    return C
