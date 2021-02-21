import functools

import torch


# noinspection PyPep8Naming
class tensored:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        annotations = func.__init__.__code__.co_varnames[1:]
        indices = {name: i for i, name in enumerate(annotations)}

        def getattribute(self, name):
            return self[indices[name]]

        self.g = getattribute

    def __call__(self, *args, **kwargs):
        instance = torch.tensor(args, dtype=torch.float32)

        class Wrapper(instance.__class__):
            pass

        instance.__class__ = Wrapper
        instance.__class__.__getattr__ = self.g

        return instance
