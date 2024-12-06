from GtkHelper.GtkHelper import better_disconnect
from ...OBSMultiActionItem import OBSMultiActionItem
from ....globals import Icons
from ....internal.MultiAction.MultiActionItem import MultiActionItem
from ....internal.ComboAction.ComboActionRow import ComboActionRow, ComboActionItem
from ....internal.DuoPreferencesRow import DuoPreferencesRow

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class SwitchScene(OBSMultiActionItem):
    FIELD_NAME = "Switch Scene"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mode_index: int = 2

        self.action_items = [
            ComboActionItem(name="Increase", callback=self.plugin_base.backend.start_replay_buffer),
            ComboActionItem(name="Decrease", callback=self.plugin_base.backend.stop_replay_buffer),
            ComboActionItem(name="Set", callback=self.plugin_base.backend.toggle_replay_buffer),
        ]

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_current_program_scene_changed",
                                                  self.program_scene_changed)

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent",
                                                  "on_current_preview_scene_changed",
                                                  self.preview_scene_changed)

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::ConnectionChange", self.connection_changed)

    # Action Events

    def on_ready(self):
        pass

    def on_update(self):
        pass

    def on_key_down(self):
        pass

    def on_tick(self):
        pass

    # Asyncs

    async def program_scene_changed(self, event_id: str, obs_event: str, message: dict):
        print(message)

    async def preview_scene_changed(self, event_id: str, obs_event: str, message: dict):
        print(message)

    async def connection_changed(self, event_id: str, obs_event: str, message: dict):
        print(message)

    async def icon_changed(self, event: str, key: str, asset):
        pass

    def color_changed(self):
        pass

    #
    # UI
    #

    def build_ui(self):
        pass

    #
    # UI EVENTS
    #

    def connect_events(self):
        pass

    def disconnect_events(self):
        pass

    #
    # SETTINGS
    #

    def load_settings(self):
        pass

    def load_ui_settings(self):
        pass

    #
    # MISC
    #

    def display_icon(self, status):
        pass