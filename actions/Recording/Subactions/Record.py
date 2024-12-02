from ....internal.MultiAction.MultiActionItem import MultiActionItem
from ....internal.ComboAction.ComboActionRow import ComboActionRow, ComboActionItem
from ....internal.DuoPreferencesRow import DuoPreferencesRow

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw


class Record(MultiActionItem):
    FIELD_NAME = "Record"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_timecode: bool = False
        self.show_pause_state: bool = False
        self.location_index: int = 0
        self.mode_index: int = 2
        self.recording_offset: int = 0

        self.primary_background = self.plugin_base.asset_manager.colors.get_asset_values("primary")
        self.secondary_background = self.plugin_base.asset_manager.colors.get_asset_values("secondary")

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

    #
    # UI
    #

    def build_ui(self):
        self.action_mode = ComboActionRow(title="Action Mode")
        self.pause_state_switch = Adw.SwitchRow(title="Show Pause State")
        self.timecode_switch = Adw.SwitchRow(title="Show Timecode", hexpand=True)
        self.timecode_location = ComboActionRow(title="Timecode Location", hexpand=True)
        self.timecode_selector = DuoPreferencesRow(self.timecode_switch, self.timecode_location)

        self.offset_spin = Adw.SpinRow.new_with_range(-10000, 10000, 1)
        self.offset_spin.set_title("Recording Offset In ms")

        self.add(self.action_mode)
        self.add(self.pause_state_switch)
        self.add(self.timecode_selector)
        self.add(self.offset_spin)

    #
    # UI EVENTS
    #

    def connect_events(self):
        self.action_mode.connect("item-changed", self.action_mode_changed)
        self.timecode_switch.connect("notify::active", self.timecode_switch_changed)
        self.timecode_location.connect("item-changed", self.timecode_location_changed)
        self.pause_state_switch.connect("notify::active", self.pause_state_switch_changed)
        self.offset_spin.connect("changed", self.offset_changed)

    def disconnect_events(self):
        try:
            self.action_mode.disconnect_by_func(self.action_mode_changed)
            self.timecode_switch.disconnect_by_func(self.timecode_switch_changed)
            self.timecode_location.disconnect_by_func(self.timecode_location_changed)
            self.pause_state_switch.disconnect_by_func(self.pause_state_switch_changed)
            self.offset_spin.disconnect_by_func(self.offset_changed)
        except:
            pass

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

    #
    # ACTION EVENTS
    #

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        status = self.plugin_base.backend.get_record_status()

        if not status:
            self.action_base.set_background_color(self.secondary_background)
            return

        self.display_icon(status)
        self.display_timecode(status)

    def on_key_down(self):
        if self.action_items[self.mode_index].callback:
            self.action_items[self.mode_index].callback()

    def on_tick(self):
        status = self.plugin_base.backend.get_record_status() or {}

        self.display_icon(status)
        self.display_timecode(status)

    #
    # SETTINGS
    #

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

    #
    # MISC
    #

    def display_icon(self, status):
        if status.get("output_active", False):
            self.action_base.set_background_color(self.primary_background)
            if status.get("output_paused", False) and self.show_pause_state:
                _, render = self.plugin_base.asset_manager.icons.get_asset_values("rec_paused")
            else:
                _, render = self.plugin_base.asset_manager.icons.get_asset_values("rec_on")
        else:
            self.action_base.set_background_color(self.secondary_background)
            _, render = self.plugin_base.asset_manager.icons.get_asset_values("rec_off")
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

    async def record_state_changed(self, event_id: str, obs_event: str, message: dict):
        self.on_tick()