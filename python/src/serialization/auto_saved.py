import functools

import torch


def auto_saved(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        instance = cls(*args, **kwargs)

        def save(path: str):
            checkpoint = instance.state_dict()
            torch.save(checkpoint, path)

        def load(path: str):
            checkpoint = torch.load(path)
            instance.load_state_dict(checkpoint)

        instance.save = save
        instance.load = load

        return instance

    return wrapper
