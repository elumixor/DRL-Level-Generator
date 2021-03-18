import inspect
import os

from common import read_yaml, to_dot_dict
from .commands import run_one
from .runner import run_experiment

defaults = read_yaml("./defaults.yaml")


def run_current(**options):
    caller_dir = os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
    config_path = os.path.join(caller_dir, defaults.config)

    run_one(config_path, to_dot_dict(options))