import obswebsocket.exceptions
from obswebsocket import obsws

from RequestFormatters.GeneralFormatters import VersionFormatter

from loguru import logger as log
import websocket

class OBSController(obsws):
    def __init__(self):
        self.connected: bool = False
        self.event_obs: obsws = None
        self.version: VersionFormatter = None

    def on_connect(self, obs: obsws):
        self.connected = True

    def on_disconnect(self, obs):
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

    def _connect(self, **kwargs):
        super().__init__(on_connect=self.on_connect, on_disconnect=self.on_disconnect, **kwargs)
        self.event_obs = obsws(on_connect=self.on_connect, on_disconnect=self.on_disconnect, **kwargs)
        self.connect()
        #self.get_version()
        #log.info(f"Successfully connected to OBS {self.version.OBS_VERSION} "
        #         f"under {kwargs.get("host")}:{kwargs.get("port")}")

    def open_connection(self, host: str = 'localhost', port: int = 4455, password: str = "", legacy: bool = False, **kwargs) -> bool:
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

    #
    # GENERAL REQUESTS
    #