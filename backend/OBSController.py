import ipaddress
from typing import Callable, Type

import obswebsocket.exceptions
from obswebsocket import obsws, events

from loguru import logger as log

from OBSEventHandler import OBSEventHandler
from Events.OBSEvent import OBSEvent
from Requests.GeneralRequests import GeneralRequest

class OBSController(obsws):
    def __init__(self):
        self.connected: bool = False
        self.handler: OBSEventHandler = None
        self.obs_event: obsws = None

    def on_connect(self, obs: obsws):
        self.connected = True

    def on_disconnect(self, obs: obsws):
        self.connected = False

    def validate_host(self, host: str):
        if host == 'localhost':
            return True
        try:
            ip = ipaddress.ip_address(host)

            if ip:
                return True
            return False
        except ValueError as e:
            log.error(e)

            log.info("Disconnecting OBSController and Event Listener")
            if self.connected:
                self.disconnect()

            return False

    def register_event(self, callback, event_name):
        self.handler.register(callback, event_name)

    def event_frontend_runner(self):
        pass

    def _connect(self, **kwargs):
        super().__init__(on_connect=self.on_connect, on_disconnect=self.on_disconnect, **kwargs)
        self.obs_event = obsws(**kwargs)

        self.connect()
        self.obs_event.connect()
        self.handler = OBSEventHandler(self.obs_event)

        version = GeneralRequest.get_version(self)
        log.info(f"Successfully connected to OBS {version.OBS_VERSION} under {kwargs.get("host"):{kwargs.get("port")}}")

    def connect_to_obs(self, host: str = 'localhost', port: int = 4455, password: str = "", legacy: bool = False, **kwargs):
        if not self.validate_host(host):
            return False
        if self.connected:
            self.disconnect()

        try:
            self._connect(host=host, port=port, password=password, legacy=legacy, **kwargs)
            return True
        except (obswebsocket.exceptions.ConnectionFailure, ValueError) as e:
            log.error(f"Failed to connect to OBS with legacy: {legacy}, trying with legacy={not legacy}!")
            try:
                self._connect(host=host, port=port, password=password, legacy=not legacy, **kwargs)
                return True
            except (obswebsocket.exceptions.ConnectionFailure, ValueError) as e:
                log.error(f"Failed to connect to OBS: {e}")
        log.error(f"Data used to connect to OBS: Host-{host} | Port-{port}")
        return False
