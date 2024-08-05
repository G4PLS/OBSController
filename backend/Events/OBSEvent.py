import asyncio


class OBSEvent:
    def __init__(self):
        self.event = None
        self.observers: list = []
        self.x: list = []

    def register(self, callback):
        if callback not in self.observers:
            self.observers.append(callback)

    def b(self, callback):
        self.x.append(callback)

    def unregister(self, callback):
        if callback in self.observers:
            self.observers.remove(callback)

    def trigger(self, message):
        for callback in self.observers:
            callback(message)

    def execute_callback(self, message):
        print("CALLING BACK")
        print(self.x)
        for callback in self.x:
            callback(message)