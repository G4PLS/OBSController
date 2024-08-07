import asyncio
import threading

import fipv
import obsws_python as obsws
from obsws_python.error import OBSSDKError

from loguru import logger as log

class OBSController:
    def __init__(self, backend):
        self.request_client: obsws.ReqClient = None
        self.event_client: obsws.EventClient = None
        self.backend = backend

    def validate_host(self, host: str):
        if host == 'localhost':
            return True
        return fipv.ipv4(host)

    def _connect(self, **kwargs):
        try:
            self.request_client = obsws.ReqClient(**kwargs)
            self.event_client = obsws.EventClient(**kwargs)
        except Exception as e:
            log.error(f"Error while connecting to OBS {e}")
            return

        version = self.request_client.get_version()
        log.info(f"Successfully connected to OBS {version.obs_version} under {kwargs.get("host"):{kwargs.get("port")}}")

    def register(self):
        print("REGISTERED")
        self.event_client.callback.register(self.on_current_program_scene_changed)

    def on_current_program_scene_changed(self, *args):
        print("ON SCENE CHANGED")
        self.backend.trigger(*args)

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