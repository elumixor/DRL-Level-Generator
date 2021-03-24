class Recorder:
    def __init__(self):
        self.entries = dict()

    def record(self, **kwargs):
        for name, value in kwargs.items():
            if name not in self.entries:
                arr = []
                self.entries[name] = arr
            else:
                arr = self.entries[name]

            arr.append(value)
