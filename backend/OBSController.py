import asyncio
import threading

import fipv
import obsws_python as obsws
from obsws_python.error import OBSSDKError

from EventController import EventController
from OBSWSConverter import to_dict

from loguru import logger as log

class OBSController:
    def __init__(self, backend):
        self.request_client: obsws.ReqClient = None
        self.event_client: EventController = None
        self.backend = backend

    def validate_host(self, host: str):
        if host == 'localhost':
            return True
        return fipv.ipv4(host)

    def _connect(self, **kwargs):
        try:
            self.request_client = obsws.ReqClient(**kwargs)
            self.event_client = EventController(frontend=self.backend.frontend, **kwargs)
            #self.event_client = EventController(frontend=None, **kwargs)
        except Exception as e:
            log.error(f"Error while connecting to OBS: {e} | Used args: {kwargs}")
            return

        version = self.request_client.get_version()
        log.info(f"Successfully connected to OBS {version.obs_version} under {kwargs.get("host"):{kwargs.get("port")}}")

    def connect_to_obs(self, host: str = 'localhost', port: int = 4455, password: str = "", timeout: int = 60, **kwargs):
        if not self.validate_host(host):
            return False

        if self.request_client:
            self.request_client.disconnect()
        if self.event_client:
            self.event_client.disconnect()

        try:
            self._connect(host=host, port=port, password=password, timeout=timeout, **kwargs)
        except OBSSDKError as e:
            log.error(f"Failed to connect to OBS: {e}")
            log.error(f"Data used to connect to OBS: Host-{host} | Port-{port}")

    def send_request(self, function_name, *args):
        try:
            if not hasattr(self.request_client, function_name):
                return

            method = getattr(self.request_client, function_name)
            if callable(method):
                return_args = method(*args)

                if hasattr(return_args, "__dict__"):
                    return to_dict(return_args)
                print(return_args)
        except OBSSDKError as e:
            log.error(f"Not able to call function: {function_name}. Error: {e}")