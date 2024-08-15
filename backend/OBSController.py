import obsws_python as obsws
from obsws_python.error import OBSSDKRequestError
from loguru import logger as log

from EventController import EventController
from OBSWSConverter import to_dict

try:
    import fipv
    fipv_import: bool = True
except ImportError as e:
    log.error("Error importing fipv, using ipaddress as fallback")
    import ipaddress
    fipv_import: bool = False

class OBSController:
    def __init__(self, backend):
        self.request_client: obsws.ReqClient = None
        self.event_client: EventController = None
        self.backend = backend
        self.connected = False

    def validate_host(self, host: str):
        if host == 'localhost':
            return True

        if fipv_import:
            return fipv.ipv4(host)
        else:
            try:
                ipaddress.ip_address(host)
                return True
            except ValueError as e:
                log.error(f"{host} is not a valid ip address")
                return False

    def on_disconnect(self, *args):
        log.info("OBS got Closed, connection is getting closed aswell")
        self.request_client.disconnect()
        self.event_client.disconnect()
        self.request_client = None
        self.event_client = None

        self.connected = False

    def _connect(self, **kwargs):
        try:
            self.request_client = obsws.ReqClient(**kwargs)
            self.event_client = EventController(frontend=self.backend.frontend, on_disconnect=self.on_disconnect, **kwargs)
            self.connected = True
        except Exception as e:
            log.error(f"Error while connecting to OBS: {e} | Used args: {kwargs}")
            self.connected = False
            return

        version = self.request_client.get_version()
        log.info(f"Successfully connected to OBS {version.obs_version} under {kwargs.get('host', 'N/A')}:{kwargs.get('port', 'N/A')}")

    def connect_to_obs(self, host: str = 'localhost', port: int = 4455, password: str = "", timeout: int = 60, **kwargs):
        if not self.validate_host(host):
            return False

        if self.request_client or self.connected:
            self.request_client.disconnect()
        if self.event_client or self.connected:
            self.event_client.disconnect()

        self.connected = False

        try:
            self._connect(host=host, port=port, password=password, timeout=timeout, **kwargs)
        except Exception as e:
            log.error(f"Failed to connect to OBS: {e}")
            log.error(f"Data used to connect to OBS: Host-{host} | Port-{port}")

    def send_request(self, function_name, *args):
        if not self.connected:
            return

        try:
            if not hasattr(self.request_client, function_name):
                return

            method = getattr(self.request_client, function_name)
            if callable(method):
                return_args = method(*args)

                if hasattr(return_args, "__dict__"):
                    return to_dict(return_args)
        except OBSSDKRequestError as e:
            log.error(f"Error while sending request: {e}")
        except Exception as e:
            log.error(f"Not able to call function: {function_name}, connection state will be set to False. Error: {e}")
            self.connected = False
        return None