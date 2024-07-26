from streamcontroller_plugin_tools import BackendBase
from OBSController import OBSController
from Requests import *

class Backend(BackendBase):
    def __init__(self):
        #super().__init__()
        self.obs_controller = OBSController()
        self.obs_controller.connect_to_obs(
            host=self.get_setting("ip", "localhost"),
            port=self.get_setting("port", 4455),
            password=self.get_setting("password", "")
        )
        #self.obs_controller.connect_to_obs()

    def get_setting(self, key: str, default=None):
        return self.frontend.get_settings().get(key, default)

    def get_connected(self) -> bool:
        return self.obs_controller.connected

    #
    # RECORD
    #

    def start_record(self):
        RecordRequests.start_record(self.obs_controller)

    def stop_record(self):
        RecordRequests.stop_record(self.obs_controller)

    def pause_record(self):
        RecordRequests.pause_record(self.obs_controller)