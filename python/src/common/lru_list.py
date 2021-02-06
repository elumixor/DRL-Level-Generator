class LRUList:
    def __init__(self, *args, capacity=100):
        self.capacity = capacity
        self.items = list(args)[:capacity]

    @property
    def size(self):
        return len(self.items)

    @property
    def is_full(self):
        return self.size == self.capacity

    def append(self, item):
        if self.is_full:
            self.items.pop(0)

        self.items.append(item)

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        yield from self.items
