class Event:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def unsubscribe(self, callback):
        self.subscribers.remove(callback)

    def invoke(self, data):
        for callback in self.subscribers:
            callback(data)

    def __call__(self, data):
        self.invoke(data)

    def __iadd__(self, callback):
        self.subscribe(callback)

    def __isub__(self, callback):
        self.unsubscribe(callback)
