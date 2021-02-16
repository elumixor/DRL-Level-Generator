import cProfile
import pstats

from .auto_logged import auto_logged
from .logger import Logger
from .q_estimator import QEstimator


class timed:
    def __init__(self, sort_by='tottime'):
        self.sort_by = sort_by

    def __enter__(self):
        self.profiler = cProfile.Profile()
        self.profiler.enable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.profiler.disable()
        pstats.Stats(self.profiler).sort_stats('tottime').print_stats()
