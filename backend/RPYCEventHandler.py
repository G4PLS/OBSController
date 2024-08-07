import rpyc

class RPYCEventHandler:
    def __init__(self, rpyc_service: rpyc.Service):
        self.rpyc_service: rpyc.Service = rpyc_service
        self.callbacks: dict[str, list[callable]] = {}

    def register_callback(self, event_name, callback: callable):
        if event_name in self.callbacks:
            self.callbacks[event_name].append(callback)
        else:
            self.callbacks[event_name] = []

    def trigger(self, event_name):
        pass
