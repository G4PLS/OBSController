import gi

from src.backend.DeckManagement.Media.Media import Media
from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from ..RecordActionHandler import RecordActionHandler

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

class RecordActionBase(RecordActionHandler):
    """
    Used for actual sub-actions specialized for Recording
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_timecode: bool = False
        self.show_pause_state: bool = True
        self.recording_offset: int = 0

        self.RECORD_ON = Media(layers=[
            ImageLayer.from_media_path(self.get_media_path("recording_dot_on.svg", subdir="Record/Dot")),
            ImageLayer.from_media_path(self.get_media_path("recording_rings_on.svg", subdir="Record/Rings"))
        ]).get_final_media()
        self.RECORD_OFF = Media(layers=[
            ImageLayer.from_media_path(self.get_media_path("recording_dot_off.svg", subdir="Record/Dot")),
            ImageLayer.from_media_path(self.get_media_path("recording_rings_off.svg", subdir="Record/Rings"))
        ]).get_final_media()
        self.RECORD_PAUSED = Media(layers=[
            ImageLayer(image=self.RECORD_ON),
            ImageLayer.from_media_path(self.get_media_path("little_pause_on.svg", subdir="Record/Pause"))
        ]).get_final_media()

    def build_ui(self) -> None:
        super().build_ui()
        self.show_pause_state_switch = Adw.SwitchRow(title="Show Pause State")
        self.show_timecode_switch = Adw.SwitchRow(title="Show Timecode")
        self.recording_offset_spin = Adw.SpinRow.new_with_range(-10000, 10000, 1)
        self.recording_offset_spin.set_title("Recording Offset in (ms)")

        self.add(self.show_pause_state_switch)
        self.add(self.show_timecode_switch)
        self.add(self.recording_offset_spin)

        self.connect_events()

    def connect_events(self):
        super().connect_events()

        self.show_timecode_switch.connect("notify::active", self.timecode_switch_changed)
        self.show_pause_state_switch.connect("notify::active", self.pause_state_switch_changed)
        self.recording_offset_spin.connect("changed", self.offset_changed)
        self.recording_offset_spin.connect("activate", self.offset_changed)

    def disconnect_events(self):
        super().disconnect_events()

        try:
            self.show_timecode_switch.disconnect_by_func(self.timecode_switch_changed)
            self.recording_offset_spin.disconnect_by_func(self.offset_changed)
            self.show_pause_state_switch.disconnect_by_func(self.pause_state_switch_changed)
        except:
            pass

    def timecode_switch_changed(self, *args):
        settings = self.action_base.get_settings()

        self.show_timecode = self.show_timecode_switch.get_active()
        settings["show-timecode"] = self.show_timecode

        self.action_base.set_settings(settings)

        self.update_button()

    def pause_state_switch_changed(self, *args):
        settings = self.action_base.get_settings()

        self.show_pause_state = self.show_pause_state_switch.get_active()
        settings["show-pause-state"] = self.show_pause_state

        self.update_button()

    def update_button(self):
        status = self.plugin_base.backend.get_record_status()

        if status is None:
            self.show_error()
            return

        self.set_record_status(status)
        self.set_timecode(status)

    def offset_changed(self, *args):
        settings = self.action_base.get_settings()

        self.recording_offset = int(self.recording_offset_spin.get_value())
        settings["recording-offset"] = self.recording_offset

        self.action_base.set_settings(settings)

    def load_settings(self):
        super().load_settings()

        settings = self.action_base.get_settings()

        self.show_timecode = settings.get("show-timecode", False)
        self.show_pause_state = settings.get("show-pause-state", False)
        self.recording_offset = settings.get("recording-offset", 0)

    def load_ui_settings(self):
        super().load_ui_settings()

        self.disconnect_events()

        self.show_timecode_switch.set_active(self.show_timecode)
        self.show_pause_state_switch.set_active(self.show_pause_state)
        self.recording_offset_spin.set_value(self.recording_offset)

        self.connect_events()

    def set_record_status(self, record_status):
        if not self.show_status:
            self.action_base.set_media(None)
            self.action_base.set_background_color([0, 0, 0, 0])
            return

        if record_status.get("output_active", False):
            if record_status.get("output_paused", False) and self.show_pause_state:
                new_image = self.RECORD_PAUSED
            else:
                new_image = self.RECORD_ON
            self.action_base.set_background_color(self.plugin_base.PRIMARY_BACKGROUND)
        else:
            new_image = self.RECORD_OFF
            self.action_base.set_background_color(self.plugin_base.SECONDARY_BACKGROUND)

        self.update_status_image(new_image)

    def set_timecode(self, record_status):
        if self.show_timecode:
            milliseconds = record_status.get("output_duration", 0)

            milliseconds += self.recording_offset
            timecode = self.milliseconds_to_timestamp(milliseconds)

            self.action_base.set_top_label(timecode)
        else:
            self.action_base.set_top_label("")

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
