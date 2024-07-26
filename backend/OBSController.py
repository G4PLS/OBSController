import ipaddress

import obswebsocket.exceptions
from obswebsocket import obsws

from loguru import logger as log
import websocket
from Requests.GeneralRequests import GeneralRequest

class OBSController(obsws):
    def __init__(self):
        self.connected: bool = False
        self.event_obs: obsws = None

    def on_connect(self, obs: obsws):
        self.connected = True

    def on_disconnect(self, obs: obsws):
        self.connected = False

    def register(self, *args, **kwargs):
        """
        Pass all event register calls to the event_obs.
        This avoids crashes if a request is made in an event
        """
        try:
            self.event_obs.register(*args, **kwargs)
        except (obswebsocket.exceptions.MessageTimeout,  websocket._exceptions.WebSocketConnectionClosedException, KeyError) as e:
            log.error(e)

    def unregister(self, *args, **kwargs):
        try:
            self.event_obs.unregister(*args, **kwargs)
        except (obswebsocket.exceptions.MessageTimeout,  websocket._exceptions.WebSocketConnectionClosedException, KeyError) as e:
            log.error(e)

    def validate_host(self, host: str):
        if host == 'localhost':
            return True
        try:
            ipaddress.ip_address(host)
            return True
        except ValueError as e:
            log.error(e)

            log.info("Disconnecting OBSController and Event Listener")
            if self.connected:
                self.disconnect()
            if (self.event_obs is not None and
                    self.event_obs.ws is not None):
                self.event_obs.disconnect()

            return False

    def _connect(self, **kwargs):
        super().__init__(on_connect=self.on_connect, on_disconnect=self.on_disconnect, **kwargs)
        self.event_obs = obsws(on_connect=self.on_connect, on_disconnect=self.on_disconnect, **kwargs)
        self.connect()
        version = GeneralRequest.get_version(self)
        log.info(f"Successfully connected to OBS {version.OBS_VERSION} under {kwargs.get("host"):{kwargs.get("port")}}")

    def connect_to_obs(self, host: str = 'localhost', port: int = 4455, password: str = "", legacy: bool = False, **kwargs):
        if not self.validate_host(host):
            return

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
        return False
