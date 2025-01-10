from src.backend.DeckManagement.InputIdentifier import InputEvent, Input
from src.backend.PluginManager.ActionBase import ActionBase
#from src.backend.Logging.Loggers.PluginLogger import plugin_logger
from GtkHelper.GtkHelper import better_disconnect
from ...globals import Icons, Colors
import gi

from GtkHelper.SearchComboRow import SearchComboRow

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ..OBSAction import OBSAction

class ToggleRecord(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_pause_state: bool = False
        self.show_timecode: bool = False
        self.recording_offset: int = 0
        self.timecode_location: str = "top"

        self.icon_keys = [Icons.REC_ON, Icons.REC_OFF, Icons.REC_PAUSED]
        self.color_keys = [Colors.PRIMARY, Colors.SECONDARY]

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_record_state_changed",
                                                  self.record_state_changed)


    # Action Events

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        self.send_obs_request()

        self.show_icon()
        self.show_label()
        self.show_color()

    def on_tick(self):
        self.send_obs_request()

        self.show_icon()
        self.show_label()
        self.show_color()

    def on_short_up(self):
        self.plugin_base.backend.toggle_record()

    # Ui Definition

    def build_ui(self):
        self.ui = Adw.PreferencesGroup(title="Toggle Record")

        self.pause_state_switch = Adw.SwitchRow(title="Show Pause State")
        self.timecode_switch = Adw.SwitchRow(title="Show Timecode")
        self.timecode_locator = SearchComboRow(title="Timecode Location", use_single_line=True)

        self.offset_spin = Adw.SpinRow.new_with_range(-10000, 10000, 1)
        self.offset_spin.set_title("Recording offset in ms")
        self.offset_spin.set_value(0)

        self.ui.add(self.pause_state_switch)
        self.ui.add(self.timecode_switch)
        self.ui.add(self.offset_spin)
        self.ui.add(self.timecode_locator)

    # Setting Loaders

    def load_settings(self):
        settings = self.get_settings()

        self.show_pause_state = settings.get("show-pause-state", False)
        self.show_timecode = settings.get("show-timecode", False)
        self.timecode_location = settings.get("timecode-location", "top")
        self.recording_offset = settings.get("recording-offset", 0)

    def load_ui_settings(self):
        self.pause_state_switch.set_active(self.show_pause_state)
        self.timecode_switch.set_active(self.show_timecode)
        self.offset_spin.set_value(self.recording_offset)

        positions = self.label_provider.generate_search_items()
        index = self.label_provider.get_index(self.timecode_location)

        self.timecode_locator.populate(positions, index)

    def send_obs_request(self):
        status = self.plugin_base.backend.get_record_status() or {}
        self.change_icon(status)
        self.change_timecode(status)
        self.change_color(status)

    # Ui Events

    def connect_events(self):
        self.pause_state_switch.connect("notify::active", self.show_pause_state_changed)
        self.timecode_switch.connect("notify::active", self.show_timecode_changed)
        self.timecode_locator.connect("item-changed", self.timecode_location_changed)
        self.offset_spin.connect("changed", self.offset_changed)

    def disconnect_events(self):
        better_disconnect(self.pause_state_switch, self.show_pause_state_changed)
        better_disconnect(self.timecode_switch, self.show_timecode_changed)
        better_disconnect(self.offset_spin, self.offset_changed)
        better_disconnect(self.timecode_locator, self.timecode_location_changed)

    def show_pause_state_changed(self, *args):
        settings = self.get_settings()
        state = self.pause_state_switch.get_active()

        self.show_pause_state = state
        settings["show-pause-state"] = state
        self.set_settings(settings)

        self.show_icon()

    def show_timecode_changed(self, *args):
        settings = self.get_settings()
        state = self.timecode_switch.get_active()

        self.show_timecode = state
        settings["show-timecode"] = state
        self.set_settings(settings)

        self.show_label()

    def timecode_location_changed(self, _, item, *args):
        settings = self.get_settings()
        location = item.display_label

        self._current_labels[self.timecode_location] = ""
        self._current_labels[location] = self.last_timecode
        self.timecode_location = location
        settings["timecode-location"] = location
        self.set_settings(settings)

        self.show_label()

    def offset_changed(self, *args):
        settings = self.get_settings()
        offset = self.offset_spin.get_value()

        self.recording_offset = offset
        settings["recording-offset"] = offset
        self.set_settings(settings)

        self.change_timecode(None)

    # Displaying

    def change_color(self, status):
        if status.get("output_active", False):
            self._color_name = Colors.PRIMARY
        else:
            self._color_name = Colors.SECONDARY
        self._current_color = self.get_color(self._color_name)

    def change_icon(self, status):
        if status.get("output_active", False):
            if status.get("output_paused", False) and self.show_pause_state:
                self._icon_name = Icons.REC_PAUSED
            else:
                self._icon_name = Icons.REC_ON
        else:
            self._icon_name = Icons.REC_OFF
        self._current_icon = self.get_icon(self._icon_name)

    def change_timecode(self, status):
        if self.show_timecode and status:
            milliseconds = status.get("output_duration", 0)

            milliseconds += self.recording_offset
            self.last_timecode = self.milliseconds_to_timestamp(milliseconds)
        else:
            self.last_timecode = ""

        self._current_labels[self.timecode_location] = self.last_timecode

    # Asset Managing

    async def record_state_changed(self, event_id: str, obs_event: str, message: dict):
        status = {}

        status_mapping = {
            "OBS_WEBSOCKET_OUTPUT_STARTED":  {"running":True, "paused": False},
            "OBS_WEBSOCKET_OUTPUT_STARTING": {"running":True, "paused": False},
            "OBS_WEBSOCKET_OUTPUT_RESUMED":  {"running":True, "paused": False},
            "OBS_WEBSOCKET_OUTPUT_STOPPING": {"running":False, "paused": False},
            "OBS_WEBSOCKET_OUTPUT_STOPPED":  {"running":False, "paused": False},
            "OBS_WEBSOCKET_OUTPUT_PAUSED":   {"running":True, "paused": True},
        }

        state = message.get("output_state", "OBS_WEBSOCKET_OUTPUT_STOPPED")

        mapped_state = status_mapping.get(state, {})

        status["output_active"] = mapped_state.get("running", False)
        status["output_paused"] = mapped_state.get("paused", False)

        self.change_icon(status)
        self.change_color(status)
        self.show_icon()
        self.show_color()

    # Misc

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
