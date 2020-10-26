class Buffer:
    def __init__(self, max_size):
        self.elements = []
        self.max_size = max_size

    def push(self, x):
        self.elements.append(x)
        if len(self.elements) > self.max_size:
            self.elements.pop(0)

    def __len__(self):
        len(self.elements)

    def __iter__(self):
        return iter(self.elements)

    def __str__(self):
        return str(self.elements)

    def __getitem__(self, i):
        return self.elements[i]
