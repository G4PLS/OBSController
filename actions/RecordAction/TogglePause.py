from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionBase import ActionBase

from ..SubAction import SubAction

class TogglePause(SubAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("REGISTERING")
        self.plugin_base.register_event("on_current_program_scene_changed", self.a)
        self.plugin_base.register_event("on_exit_started", self.b)

    def a(self, *args):
        x = 0
        while x < 9848894:
            print(x)
            x += 1

        print("A")
        print(args[0].get("scene_name", "NO"))

    def b(self, *args):
        while True:
            print("IM A VERY LONG TEXT")