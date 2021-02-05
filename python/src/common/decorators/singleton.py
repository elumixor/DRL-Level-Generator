from functools import update_wrapper


# Used as a decorator
class singleton:
    def __init__(self, ctor):
        update_wrapper(self, ctor)
        self._instance = None
        self.ctor = ctor

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self.ctor(*args, **kwargs)

        return self._instance

    @property
    def instance(self):
        if self._instance is None:
            self._instance = self.ctor()

        return self._instance
