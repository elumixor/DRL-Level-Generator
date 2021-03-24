import torch


def tensored(_func=None):
    # noinspection PyPep8Naming
    class wrapper:
        def __init__(self, func):
            annotations = func.__init__.__code__.co_varnames[1:]
            indices = {name: i for i, name in enumerate(annotations)}

            def getattribute(self, name):
                if name in indices:
                    return self[indices[name]]

                return super(torch.Tensor, self).__getattr__(name)

            self.g = getattribute
            self.size = len(annotations)

        def __len__(self):
            return self.size

        def __call__(self, *args, **kwargs):
            instance = torch.tensor(args, dtype=torch.float32)

            class Wrapper(instance.__class__):
                ...

            instance.__class__ = Wrapper
            instance.__class__.__getattr__ = self.g

            return instance

    if _func is None:
        return wrapper  # 2
    else:
        return wrapper(_func)  # 3
