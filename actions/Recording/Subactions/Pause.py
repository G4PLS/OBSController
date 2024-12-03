from GtkHelper.GtkHelper import better_disconnect
from ...OBSMultiActionItem import OBSMultiActionItem
from ....internal.MultiAction.MultiActionItem import MultiActionItem
from ....internal.ComboAction.ComboActionRow import ComboActionRow, ComboActionItem

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ....globals import Icons, Colors

class Pause(OBSMultiActionItem):
    FIELD_NAME = "Pause"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.update_with_obs: bool = True
        self.mode_index: int = 2

        self.action_items = [
            ComboActionItem(name="Pause", callback=self.plugin_base.backend.pause_record),
            ComboActionItem(name="Unpause", callback=self.plugin_base.backend.resume_record),
            ComboActionItem(name="Toggle", callback=self.plugin_base.backend.toggle_pause),
        ]

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_record_state_changed",
                                                  self.record_state_changed)

    # Action Events

    def on_ready(self):
        self.load_settings()

    def on_key_down(self):
        if self.action_items[self.mode_index].callback:
            self.action_items[self.mode_index].callback()

    def on_tick(self):
        status = self.plugin_base.backend.get_record_status() or {}

        self.display_icon(status)

    # Asyncs

    async def icon_changed(self, event: str, key: str, asset):
        if key in [Icons.PAUSED, Icons.UNPAUSED]:
            self.on_tick()

    def color_changed(self):
        self.on_tick()

    async def record_state_changed(self, event_id: str, obs_event: str, message: dict):
        self.on_tick()

    #
    # UI
    #

    def build_ui(self):
        self.action_mode = ComboActionRow(title="Action Mode")
        self.update_switch = Adw.SwitchRow(title="Update Pause State with OBS",
                                                    tooltip_text="When this is active the button will change the Icon based on the current paused state in obs")

        self.add(self.action_mode)
        self.add(self.update_switch)

    #
    # UI EVENTS
    #

    def connect_events(self):
        self.action_mode.connect("item-changed", self.action_mode_changed)
        self.update_switch.connect("notify::active", self.update_switch_changed)

    def disconnect_events(self):
        better_disconnect(self.action_mode, self.action_mode_changed)
        better_disconnect(self.update_switch, self.update_switch_changed)

    def action_mode_changed(self, object, item, index):
        settings = self.get_settings()

        self.mode_index = index
        settings["mode-index"] = self.mode_index

        self.set_settings(settings)

    def update_switch_changed(self, *args):
        settings = self.action_base.get_settings()

        self.update_with_obs = self.update_switch.get_active()
        settings["update-with-obs"] = self.update_with_obs

        self.set_settings(settings)

    # SETTINGS

    def load_settings(self):
        settings = self.get_settings()

        self.mode_index = settings.get("mode-index", 2)
        self.update_with_obs = settings.get("update-with-obs", True)

    def load_ui_settings(self):
        self.disconnect_events()

        self.action_mode.set_model_items(self.action_items, self.mode_index)
        self.update_switch.set_active(self.update_with_obs)

    #
    # MISC
    #

    def display_icon(self, status):
        paused = status.get("output_paused", False)

        if paused and self.update_with_obs:
            self.action_base.set_background_color(self.primary_color)
            _, render = self.plugin_base.asset_manager.icons.get_asset_values(Icons.PAUSED)
        else:
            self.action_base.set_background_color(self.secondary_color)
            _, render = self.plugin_base.asset_manager.icons.get_asset_values(Icons.UNPAUSED)

        self.action_base.set_media(image=render)