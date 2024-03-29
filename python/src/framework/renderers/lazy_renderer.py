from torch import Tensor


class LazyRenderer:
    def __init__(self):
        self.initialized = False

    def render(self, state: Tensor, to_image=False, resolution=1):
        if not self.initialized:
            self.lazy_init(state)
            self.initialized = True

    def lazy_init(self, state):
        pass
