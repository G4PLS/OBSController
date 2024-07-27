from streamcontroller_plugin_tools import BackendBase
from OBSController import OBSController
from Requests import *
from loguru import logger as log

class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        log.warning("STARTING BACKEND")
        self.obs_controller = OBSController()
        self.obs_controller.connect_to_obs(
            host=self.get_setting("ip", "localhost"),
            port=self.get_setting("port", 4455),
            password=self.get_setting("password", "")
        )

    def get_setting(self, key: str, default=None):
        return self.frontend.get_settings().get(key, default)

    def get_connected(self) -> bool:
        return self.obs_controller.connected

    #
    # RECORD
    #
    def get_record_status(self):
        return RecordRequests.get_record_status(self.obs_controller)

    def start_record(self):
        RecordRequests.start_record(self.obs_controller)

    def stop_record(self):
        RecordRequests.stop_record(self.obs_controller)

    def pause_record(self):
        RecordRequests.pause_record(self.obs_controller)

    def resume_record(self):
        RecordRequests.resume_record(self.obs_controller)

    def toggle_record(self):
        return RecordRequests.toggle_record(self.obs_controller)

    def toggle_pause(self):
        RecordRequests.toggle_pause(self.obs_controller)

    def split_record_file(self):
        RecordRequests.split_record_file(self.obs_controller)

    #
    # STREAM
    #

    def get_stream_status(self):
        return StreamRequests.get_stream_status(self.obs_controller)

    def start_stream(self):
        StreamRequests.start_stream(self.obs_controller)

    def stop_stream(self):
        StreamRequests.stop_stream(self.obs_controller)

    def toggle_stream(self):
        StreamRequests.toggle_stream(self.obs_controller)

backend = Backend()