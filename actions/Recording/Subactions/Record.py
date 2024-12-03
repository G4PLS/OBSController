from ...OBSMultiActionItem import OBSMultiActionItem
from ....internal.ComboAction.ComboActionRow import ComboActionRow, ComboActionItem
from ....internal.AdwGrid import AdwGrid
from ....globals import Icons, Colors
from GtkHelper.GtkHelper import better_disconnect

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw


class Record(OBSMultiActionItem):
    FIELD_NAME = "Record"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_timecode: bool = False
        self.show_pause_state: bool = False
        self.location_index: int = 0
        self.mode_index: int = 2
        self.recording_offset: int = 0

        self.last_timecode: str = "00:00:00"

        self.location_items = [
            ComboActionItem(name="Top", callback=self.action_base.set_top_label),
            ComboActionItem(name="Bottom", callback=self.action_base.set_bottom_label)
        ]

        self.action_items = [
            ComboActionItem(name="Start", callback=self.plugin_base.backend.start_record),
            ComboActionItem(name="Stop", callback=self.plugin_base.backend.stop_record),
            ComboActionItem(name="Toggle", callback=self.plugin_base.backend.toggle_record),
        ]

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_record_state_changed",
                                                  self.record_state_changed)

    # Action Events

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        status = self.plugin_base.backend.get_record_status() or {}

        self.display_icon(status)
        self.display_timecode(status)

    def on_key_down(self):
        if self.action_items[self.mode_index].callback:
            self.action_items[self.mode_index].callback()

    def on_tick(self):
        status = self.plugin_base.backend.get_record_status() or {}

        self.display_icon(status)
        self.display_timecode(status)

    # ASYNCS

    async def record_state_changed(self, event_id: str, obs_event: str, message: dict):
        self.on_tick()

    async def icon_changed(self, event: str, key: str, asset):
        if key in [Icons.REC_ON, Icons.REC_OFF, Icons.REC_PAUSED]:
            self.on_tick()

    def color_changed(self):
        self.on_tick()

    # UI

    def build_ui(self):
        self.action_mode = ComboActionRow(title="Action Mode")
        self.pause_state_switch = Adw.SwitchRow(title="Show Pause State")
        self.timecode_switch = Adw.SwitchRow(title="Show Timecode", hexpand=True)
        self.timecode_location = ComboActionRow(title="Timecode Location", hexpand=True)

        timecode_grid = AdwGrid()
        timecode_grid.add_widget(self.timecode_switch, 0, 0)
        timecode_grid.add_widget(self.timecode_location, 1, 0)

        self.offset_spin = Adw.SpinRow.new_with_range(-10000, 10000, 1)
        self.offset_spin.set_title("Recording Offset In ms")

        self.add(self.action_mode)
        self.add(self.pause_state_switch)
        self.add(timecode_grid)
        self.add(self.offset_spin)

    # UI Events

    def connect_events(self):
        self.action_mode.connect("item-changed", self.action_mode_changed)
        self.timecode_switch.connect("notify::active", self.timecode_switch_changed)
        self.timecode_location.connect("item-changed", self.timecode_location_changed)
        self.pause_state_switch.connect("notify::active", self.pause_state_switch_changed)
        self.offset_spin.connect("changed", self.offset_changed)

    def disconnect_events(self):
        better_disconnect(self.action_mode, self.action_mode_changed)
        better_disconnect(self.timecode_switch, self.timecode_switch_changed)
        better_disconnect(self.timecode_location, self.timecode_location_changed)
        better_disconnect(self.pause_state_switch, self.pause_state_switch_changed)
        better_disconnect(self.offset_spin, self.offset_changed)

    def action_mode_changed(self, object, item, index):
        settings = self.get_settings()

        self.mode_index = index
        settings["mode-index"] = self.mode_index

        self.set_settings(settings)

    def timecode_switch_changed(self, *args):
        settings = self.get_settings()

        self.show_timecode = self.timecode_switch.get_active()
        settings["show-timecode"] = self.show_timecode

        self.set_settings(settings)

    def timecode_location_changed(self, object, item, index):
        settings = self.get_settings()

        self.location_items[self.location_index].callback("")

        self.location_index = index
        settings["location_index"] = self.location_index

        self.set_timecode_label()

        self.set_settings(settings)

    def pause_state_switch_changed(self, *args):
        settings = self.get_settings()

        self.show_pause_state = self.pause_state_switch.get_active()
        settings["show-pause-state"] = self.show_pause_state

        self.set_settings(settings)

    def offset_changed(self, *args):
        settings = self.get_settings()

        self.recording_offset = int(self.offset_spin.get_value())
        settings["recording-offset"] = self.recording_offset

        self.set_settings(settings)

    # Settings

    def load_settings(self):
        settings = self.get_settings()

        self.mode_index = settings.get("mode-index", 2)
        self.show_timecode = settings.get("show-timecode", False)
        self.location_index = settings.get("location-index", 0)
        self.show_pause_state = settings.get("show-pause-state", False)
        self.recording_offset = settings.get("recording-offset", 0)

    def load_ui_settings(self):
        self.disconnect_events()

        self.action_mode.set_model_items(self.action_items, self.mode_index)
        self.timecode_switch.set_active(self.show_timecode)
        self.timecode_location.set_model_items(self.location_items, self.location_index)
        self.pause_state_switch.set_active(self.show_pause_state)
        self.offset_spin.set_value(self.recording_offset)

    # MISC

    def display_icon(self, status):
        if status.get("output_active", False):
            self.action_base.set_background_color(self.primary_color)
            if status.get("output_paused", False) and self.show_pause_state:
                _, render = self.plugin_base.asset_manager.icons.get_asset_values(Icons.REC_PAUSED)
            else:
                _, render = self.plugin_base.asset_manager.icons.get_asset_values(Icons.REC_ON)
        else:
            self.action_base.set_background_color(self.secondary_color)
            _, render = self.plugin_base.asset_manager.icons.get_asset_values(Icons.REC_OFF)
        self.action_base.set_media(image=render)

    def display_timecode(self, record_status):
        if self.show_timecode:
            milliseconds = record_status.get("output_duration", 0)

            milliseconds += self.recording_offset
            self.last_timecode = self.milliseconds_to_timestamp(milliseconds)
        else:
            self.last_timecode = ""

        self.set_timecode_label()

    def set_timecode_label(self):
        if self.location_items[self.location_index].callback:
            self.location_items[self.location_index].callback(self.last_timecode)
        else:
            self.action_base.set_top_label(self.last_timecode)

    def milliseconds_to_timestamp(self, milliseconds: int, add_milliseconds: bool = False):
        hours = milliseconds // (3600 * 1000)
        milliseconds %= (3600 * 1000)

        minutes = milliseconds // (60 * 1000)
        milliseconds %= (60 * 1000)

        seconds = milliseconds // 1000
        milliseconds %= 1000

        out = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

        if add_milliseconds:
            out += f".{int(milliseconds):03}"

        return out