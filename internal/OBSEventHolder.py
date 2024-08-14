import asyncio

from loguru import logger as log
from src.backend.PluginManager.EventHolder import EventHolder


class OBSEventHolder(EventHolder):
    def __init__(self, plugin_base: "PluginBase", event_id: str):
        if event_id in ["", None]:
            raise ValueError("Please specify an signal id")

        self.plugin_base = plugin_base
        self.event_id = event_id

        self.observers: dict[str, list[callable]] = {}

    def add_listener(self, obs_event_name: str, callback: callable):
        if not self.observers.__contains__(obs_event_name):
            self.observers[obs_event_name] = []

        if self.observers[obs_event_name].__contains__(callback):
            log.error(f"Callback: {callback.__name__} already exists for obs event: {obs_event_name}")
            return
        self.observers[obs_event_name].append(callback)

    def remove_listener(self, obs_event_name: str, callback: callable):
        if not self.observers.__contains__(obs_event_name):
            log.error(f"{obs_event_name} does not exist")
            return

        if not self.observers[obs_event_name].__contains__(callback):
            log.error(f"Callback: {callback.__name__} is not registered under: {obs_event_name}")
            return

        self.observers[obs_event_name].remove(callback)

    async def _run_event(self, *args, **kwargs):
        # args[0] = Event Name
        # args[1] = OBS Event Name
        # args[2] = OBS Event Data
        coroutines = [
            self._ensure_coroutine(observer, *args, **kwargs)
            for observer in self.observers.get(args[1], [])
        ]
        await asyncio.gather(*coroutines)