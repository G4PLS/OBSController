import rpyc
from loguru import logger as log
from streamcontroller_plugin_tools import BackendBase

from OBSController import OBSController

rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        log.info("STARTING OBS BACKEND")
        self.obs_controller = OBSController(self)
        self.obs_controller.connect_to_obs(
            host=self.get_setting("ip-address", "localhost"),
            port=self.get_setting("port", 4455),
            password=self.get_setting("password", "")
        )

    def get_setting(self, key: str, default=None):
        return self.frontend.get_settings().get(key, default)

    def get_connected(self) -> bool:
        return self.obs_controller.connected

    def reconnect(self):
        self.obs_controller.connect_to_obs(
            host=self.get_setting("ip-address", "localhost"),
            port=self.get_setting("port", 4455),
            password=self.get_setting("password", "")
        )

    #
    # RECORDING
    #

    def get_record_status(self):
        return self.obs_controller.send_request("get_record_status")

    def toggle_record(self):
        return self.obs_controller.send_request("toggle_record")

    def start_record(self):
        self.obs_controller.send_request("start_record")

    def stop_record(self):
        return self.obs_controller.send_request("stop_record")

    def toggle_pause(self):
        self.obs_controller.send_request("toggle_record_pause")

    def pause_record(self):
        self.obs_controller.send_request("pause_record")

    def resume_record(self):
        self.obs_controller.send_request("resume_record")

    def split_record_file(self):
        self.obs_controller.send_request("split_record_file")

    def create_record_chapter(self, chapter_name):
        self.obs_controller.send_request("create_record_chapter", chapter_name)

backend = Backend()