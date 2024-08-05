from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionBase import ActionBase

from ..SubAction import SubAction

class TogglePause(SubAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_click(self):
        self.plugin_base.backend.toggle_pause()

    def on_tick(self):
        record_state = self.plugin_base.backend.get_record_status()

        if record_state.PAUSED:
            self.action_base.set_top_label("PAUSED")
        else:
            self.action_base.set_top_label("NOT\nPAUSED")