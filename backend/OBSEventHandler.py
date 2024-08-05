from typing import Type

from obswebsocket import obsws
from Events import *
from Events.OBSEvent import OBSEvent
from loguru import logger as log

class OBSEventHandler:
    def __init__(self, obs: obsws):
        self.event_mapping = self.create_event_mapping()
        self.register_all(obs)

    def register_all(self, obs: obsws):
        for key, value in self.event_mapping.items():
            obs.register(value.trigger, value.event)

    def register(self, callback, event_name: str):
        event_cls = self.event_mapping.get(event_name)

        if event_cls is None:
            log.error(f"Event class for {event_name} not found")
            return

        try:
            event_cls.register(callback)
        except Exception as e:
            log.error(f"Error while registering event: {event_cls.event}. Error: {e}")

    def create_event_mapping(self):
        event_classes = OBSEvent.__subclasses__()
        return {cls.__name__: cls() for cls in event_classes}