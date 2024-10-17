from ....internal.MultiAction.MultiActionItem import MultiActionItem
from ....internal.ComboAction.ComboActionRow import ComboActionRow, ComboActionItem
from ....internal.DuoPreferencesRow import DuoPreferencesRow

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw


class StatusDisplay(MultiActionItem):
    FIELD_NAME = "Status Display"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_timecode: bool = False
        self.location_index: int = 0

        self.last_timecode: str = "00:00:00"

        self.location_items = [
            ComboActionItem(name="Top", callback=self.action_base.set_top_label),
            ComboActionItem(name="Center", callback=self.action_base.set_center_label),
            ComboActionItem(name="Bottom", callback=self.action_base.set_bottom_label)
        ]

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_record_state_changed",
                                                  self.record_state_changed)

    #
    # UI
    #

    def build_ui(self):
        self.timecode_switch = Adw.SwitchRow(title="Show Timecode", hexpand=True)
        self.timecode_location = ComboActionRow(title="Timecode Location", hexpand=True)
        self.timecode_selector = DuoPreferencesRow(self.timecode_switch, self.timecode_location)

        self.add(self.timecode_selector)

    #
    # UI EVENTS
    #

    def connect_events(self):
        self.timecode_switch.connect("notify::active", self.timecode_switch_changed)
        self.timecode_location.connect("item-changed", self.timecode_location_changed)

    def disconnect_events(self):
        try:
            self.timecode_switch.disconnect_by_func(self.timecode_switch_changed)
            self.timecode_location.disconnect_by_func(self.timecode_location_changed)
        except:
            pass

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

    #
    # ACTION EVENTS
    #

    def on_ready(self):
        self.load_settings()

    def on_tick(self):
        status = self.plugin_base.backend.get_record_status()

        if not status:
            self.action_base.set_background_color(self.plugin_base.asset_manager.SECONDARY_BACKGROUND)
            return

        self.display_icon(status)
        self.display_timecode(status)

    #
    # SETTINGS
    #

    def load_settings(self):
        settings = self.get_settings()

        self.show_timecode = settings.get("show-timecode", False)
        self.location_index = settings.get("location-index", 0)

    def load_ui_settings(self):
        self.disconnect_events()

        self.timecode_switch.set_active(self.show_timecode)
        self.timecode_location.set_model_items(self.location_items, self.location_index)

    #
    # MISC
    #

    def display_icon(self, status):
        if status.get("output_active", True):
            self.action_base.set_background_color(self.plugin_base.asset_manager.PRIMARY_BACKGROUND)
            if status.get("output_paused", False):
                self.action_base.set_media(image=self.plugin_base.asset_manager.RECORD_PAUSED_MEDIA)
            else:
                self.action_base.set_media(image=self.plugin_base.asset_manager.RECORD_ON_MEDIA)
        else:
            self.action_base.set_background_color(self.plugin_base.asset_manager.SECONDARY_BACKGROUND)
            self.action_base.set_media(image=self.plugin_base.asset_manager.RECORD_OFF_MEDIA)

    def display_timecode(self, record_status):
        if self.show_timecode:
            milliseconds = record_status.get("output_duration", 0)

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