import inspect
import os

import yaml

from .dot_dict import to_dot_dict


def read_yaml(path: str):
    # We'll try all these paths in case some do not work
    def paths():
        yield path
        yield f"{path}.yaml"
        caller_path = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[2][1])), path)
        yield caller_path
        yield f"{caller_path}.yaml"

    for p in paths():
        try:
            with open(p, "r") as stream:
                result = yaml.safe_load(stream)
                return to_dot_dict(result)
        except FileNotFoundError as e:
            ...

    # If no path worked, re-raise the last exception
    raise e
