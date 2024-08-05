import asyncio

from obswebsocket import events
from Events.OBSEvent import OBSEvent

class RecordStateChanged(OBSEvent):
    def __init__(self):
        self.event = events.RecordStateChanged
        self.observers = []
        self.x = []