from ..StreamActionHandler import StreamActionHandler

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

class StreamActionBase(StreamActionHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_timecode: bool = False
        self.show_special_icons: bool = True
        self.streaming_offset: int = 0

        self.build_ui()

    def build_ui(self) -> None:
        super().build_ui()

        self.show_timecode_switch = Adw.SwitchRow(title="Show Timecode")
        self.show_special_icon_switch = Adw.SwitchRow(title="Show Special Icon", tooltip_text="Displays the current Streaming service with the Status Icon")
        self.streaming_offset_spin = Adw.SpinRow.new_with_range(-10000, 10000, 1)
        self.streaming_offset_spin.set_title("Recording Offset in (ms)")

        self.add(self.show_special_icon_switch)
        self.add(self.show_timecode_switch)
        self.add(self.streaming_offset_spin)

        self.connect_events()

    def connect_events(self):
        super().connect_events()

        self.show_timecode_switch.connect("notify::active", self.timecode_switch_changed)
        self.show_special_icon_switch.connect("notify::active", self.special_icon_switch_changed)
        self.streaming_offset_spin.connect("changed", self.offset_changed)
        self.streaming_offset_spin.connect("activate", self.offset_changed)

    def disconnect_events(self):
        super().disconnect_events()

        try:
            self.show_timecode_switch.disconnect_by_func(self.timecode_switch_changed)
            self.show_special_icon_switch.disconnect_by_func(self.special_icon_switch_changed)
            self.streaming_offset_spin.disconnect_by_func(self.offset_changed)
        except:
            pass

    def timecode_switch_changed(self, *args):
        settings = self.action_base.get_settings()

        self.show_timecode = self.show_timecode_switch.get_active()
        settings["show-timecode"] = self.show_timecode

        self.action_base.set_settings(settings)

        self.update_button()

    def offset_changed(self, *args):
        settings = self.action_base.get_settings()

        self.streaming_offset = int(self.streaming_offset_spin.get_value())
        settings["streaming-offset"] = self.streaming_offset

        self.action_base.set_settings(settings)

    def special_icon_switch_changed(self, *args):
        settings = self.action_base.get_settings()

        self.show_special_icons = self.show_special_icon_switch.get_active()
        settings["show-special-icon"] = self.show_special_icons

        self.action_base.set_settings(settings)

    def update_button(self):
        status = self.plugin_base.backend.get_stream_status()

        if status is None:
            self.show_error()
            return

        self.set_stream_status(status)
        self.set_timecode(status)

    def load_settings(self):
        super().load_settings()

        settings = self.action_base.get_settings()

        self.show_timecode = settings.get("show-timecode", False)
        self.show_special_icons = settings.get("show-special-icon", True)
        self.streaming_offset = settings.get("streaming-offset", 0)

    def load_ui_settings(self):
        super().load_ui_settings()

        self.disconnect_events()

        self.show_timecode_switch.set_active(self.show_timecode)
        self.show_special_icon_switch.set_active(self.show_special_icons)
        self.streaming_offset_spin.set_value(self.streaming_offset)

        self.connect_events()

    def set_stream_status(self, stream_status):
        if not self.show_status:
            self.action_base.set_media(None)
            self.action_base.set_background_color([0, 0, 0, 0])
            return

        subdir = self.ASSET_SUBDIR

        if self.show_special_icons:
            stream_settings: dict = self.plugin_base.backend.get_stream_service_settings()

            if stream_settings:
                service = stream_settings.get("stream_service_settings", {}).get("service", "")

                lookup = {
                    "YouTube - RTMPS": "Youtube",
                    "Twitch": "Twitch"
                }

        if stream_status.get("output_active", False):
            if stream_status.get("output_reconnecting", False):
                new_image = "reconnecting.svg"
            else:
                new_image = "stream_on.svg"
            self.action_base.set_background_color(self.plugin_base.PRIMARY_BACKGROUND)
        else:
            new_image = "stream_off.svg"
            self.action_base.set_background_color(self.plugin_base.SECONDARY_BACKGROUND)

        self.update_status_image(new_image, "Stream")

    def set_timecode(self, stream_status):
        if self.show_timecode:
            milliseconds = stream_status.get("output_duration", 0)

            milliseconds += self.streaming_offset
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
