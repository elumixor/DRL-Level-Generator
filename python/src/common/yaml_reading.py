import yaml

from .dot_dict import to_dot_dict


class read_yaml:
    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        try:
            with open(self.path, "r") as stream:
                result = yaml.safe_load(stream)
        except FileNotFoundError:
            with open(f"{self.path}.yaml", "r") as stream:
                result = yaml.safe_load(stream)

        return to_dot_dict(result)

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
