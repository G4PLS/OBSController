

class EventMessage:
    def __init__(self, data:dict):
        self.data = data

    def get(self, key, default=None):
        if self.data.__contains__(key):
            return self.data[key]
        return default