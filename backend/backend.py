from streamcontroller_plugin_tools import BackendBase
from OBSController import OBSController
from loguru import logger as log
import rpyc
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

    def test_connection(self):
        self.obs_controller.connect_to_obs(
            host=self.get_setting("ip-address", "localhost"),
            port=self.get_setting("port", 4455),
            password=self.get_setting("password", "")
        )

    #
    # RECORDING
    #

    def get_record_status(self):
        return self.obs_controller.get_record_status()

    def toggle_record(self):
        return self.obs_controller.toggle_record()

    def start_record(self):
        self.obs_controller.start_record()

    def stop_record(self):
        return self.obs_controller.stop_record()

    def toggle_pause(self):
        self.obs_controller.toggle_record_pause()

    def pause_record(self):
        self.obs_controller.pause_record()

    def resume_record(self):
        self.obs_controller.resume_record()

    def split_record_file(self):
        self.obs_controller.split_record_file()

    def create_record_chapter(self, chapter_name):
        self.obs_controller.create_record_chapter(chapter_name)

backend = Backend()