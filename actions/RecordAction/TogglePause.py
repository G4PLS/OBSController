from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionBase import ActionBase

from ..SubAction import SubAction

class TogglePause(SubAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("REGISTERING")
        self.plugin_base.connect_to_event("com.gapls.OBSController::OBSEvent", self.a)

    def a(self, event_id: str, obs_event_name: str, message: dict):
        print(message.get("scene_name"))

    def b(self, *args):
        while True:
            print("IM A VERY LONG TEXT")