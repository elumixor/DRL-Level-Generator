import functools
from typing import Optional, List


def auto_serialized(_func=None, *, skip: Optional[List[str]] = None, include: Optional[List[str]] = None):
    if skip is None:
        skip = []

    if include is None:
        include = []

    class SF:
        def __init__(self, func):
            functools.update_wrapper(self, func)
            self.func = func

        def __call__(self, *args, **kwargs):
            instance = self.func(*args, **kwargs)

            def state_dict():
                attributes = [attr for attr in dir(instance) if
                              not attr.startswith("_") and
                              not callable(getattr(instance, attr)) and
                              attr not in skip] + include
                checkpoint = dict()
                for attr in attributes:
                    value = getattr(instance, attr)

                    if hasattr(value, "state_dict"):
                        d = getattr(value, "state_dict")
                        if callable(d):
                            serialized = d()
                        else:
                            serialized = d

                    else:
                        serialized = value

                    checkpoint[attr] = serialized

                return checkpoint

            def load_state_dict(checkpoint: dict):

                for attr, serialized in checkpoint.items():
                    value = getattr(instance, attr)

                    if hasattr(value, "load_state_dict"):
                        lsd = getattr(value, "load_state_dict")
                        if callable(lsd):
                            lsd(serialized)
                    else:
                        try:
                            setattr(instance, attr, serialized)
                        except AttributeError:
                            pass

            instance.state_dict = state_dict
            instance.load_state_dict = load_state_dict

            return instance

    if _func is None:
        return SF
    else:
        return SF(_func)
