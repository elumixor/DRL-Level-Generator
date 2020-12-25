import random
from typing import Union, TypeVar, Generic, List

T = TypeVar('T')


class MemoryBuffer(Generic[T]):

    def __init__(self, capacity: Union[int, None] = None):
        self.data: List[T] = []
        self.capacity = capacity
        self.position = 0

    @property
    def size(self):
        return len(self.data)

    @property
    def is_full(self):
        return self.capacity is None or self.size == self.capacity

    def push(self, item: T):
        if not self.is_full:
            self.data.append(item)
        else:
            self.data[self.position] = item

        if self.capacity is not None:
            self.position = (self.position + 1) % self.capacity

    def sample(self, size: int) -> List[T]:
        # If size is less than self.capacity, this will throw an error...
        # Should we train on the same samples multiple times?
        if size >= self.size:
            raise RuntimeError(f'Trying to sample a batch with size: {size},'
                               f' which is greater than the current stored number of samples: {self.size}.'
                               f' Will return a sample of size {self.size}')
        return random.sample(self.data, size)
