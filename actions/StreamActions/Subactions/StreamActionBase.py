from copy import deepcopy

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ..StreamActionHandler import StreamActionHandler

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

class StreamActionBase(StreamActionHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_timecode: bool = False
        self.show_special_icons: bool = True
        self.streaming_offset: int = 0
        self.size: float = 1.0
        self.halign: float = 0.0
        self.valign: float = 0.0

        self.build_ui()

    def build_ui(self) -> None:
        super().build_ui()

        self.show_timecode_switch = Adw.SwitchRow(title="Show Timecode")
        self.show_special_icon_switch = Adw.SwitchRow(title="Show Special Icon", tooltip_text="Displays the current Streaming service with the Status Icon")
        self.streaming_offset_spin = Adw.SpinRow.new_with_range(-10000, 10000, 1)
        self.streaming_offset_spin.set_title("Recording Offset in (ms)")

        self.image_transform = Adw.PreferencesRow()
        self.image_transform_box = Gtk.Box()
        self.image_transform.set_child(self.image_transform_box)

        self.size_spin = Adw.SpinRow.new_with_range(0, 1, 0.1)
        self.size_spin.set_title("Size")
        self.image_transform_box.append(self.size_spin)

        self.halign_spin = Adw.SpinRow.new_with_range(-1, 1, 0.1)
        self.halign_spin.set_title("HAlign")
        self.image_transform_box.append(self.halign_spin)

        self.valign_spin = Adw.SpinRow.new_with_range(-1, 1, 0.1)
        self.valign_spin.set_title("VAlign")
        self.image_transform_box.append(self.valign_spin)

        self.add(self.show_special_icon_switch)
        self.add(self.show_timecode_switch)
        self.add(self.streaming_offset_spin)
        self.add(self.image_transform)

        self.connect_events()

    def connect_events(self):
        super().connect_events()

        self.show_timecode_switch.connect("notify::active", self.timecode_switch_changed)
        self.show_special_icon_switch.connect("notify::active", self.special_icon_switch_changed)
        self.streaming_offset_spin.connect("changed", self.offset_changed)
        self.streaming_offset_spin.connect("activate", self.offset_changed)
        self.size_spin.connect("changed", self.size_changed)
        self.valign_spin.connect("changed", self.valign_changed)
        self.halign_spin.connect("changed", self.halign_changed)

    def disconnect_events(self):
        super().disconnect_events()

        try:
            self.show_timecode_switch.disconnect_by_func(self.timecode_switch_changed)
            self.show_special_icon_switch.disconnect_by_func(self.special_icon_switch_changed)
            self.streaming_offset_spin.disconnect_by_func(self.offset_changed)
            self.size_spin.disconnect_by_func(self.size_changed)
            self.valign_spin.disconnect_by_func(self.valign_changed)
            self.halign_spin.disconnect_by_func(self.halign_changed)
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

    def size_changed(self, *args):
        settings = self.action_base.get_settings()

        self.size = self.size_spin.get_value()
        settings["size"] = self.size

        self.action_base.set_settings(settings)

    def valign_changed(self, *args):
        settings = self.action_base.get_settings()

        self.valign = self.valign_spin.get_value()
        settings["valign"] = self.valign

        self.action_base.set_settings(settings)

    def halign_changed(self, *args):
        settings = self.action_base.get_settings()

        self.halign = self.halign_spin.get_value()
        settings["halign"] = self.halign

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
        self.size = settings.get("size", 1.0)
        self.valign = settings.get("valign", 0.0)
        self.halign = settings.get("halign", 0.0)

    def load_ui_settings(self):
        super().load_ui_settings()

        self.disconnect_events()

        self.show_timecode_switch.set_active(self.show_timecode)
        self.show_special_icon_switch.set_active(self.show_special_icons)
        self.streaming_offset_spin.set_value(self.streaming_offset)
        self.size_spin.set_value(self.size)
        self.valign_spin.set_value(self.valign)
        self.halign_spin.set_value(self.halign)

        self.connect_events()

    def set_stream_status(self, stream_status):
        if not self.show_status:
            self.action_base.set_media(None)
            self.action_base.set_background_color([0, 0, 0, 0])
            return

        lookup = {
            "YouTube - RTMPS": "youtube.svg",
            "Twitch": "twitch.svg"
        }

        if stream_status.get("output_active", False):
            if stream_status.get("output_reconnecting", True):
                media = deepcopy(self.RECONNECTING)
            else:
                media = deepcopy(self.STREAM_ON)
            self.action_base.set_background_color(self.plugin_base.PRIMARY_BACKGROUND)
        else:
            media = deepcopy(self.STREAM_OFF)
            self.action_base.set_background_color(self.plugin_base.SECONDARY_BACKGROUND)

        if self.show_special_icons:
            stream_settings: dict = self.plugin_base.backend.get_stream_service_settings()

            if stream_settings:
                service = stream_settings.get("stream_service_settings", {}).get("service", "")

                media = self.apply_special_icon(media, lookup.get(service, None))

        self.action_base.set_media(image=media.get_final_media())

    def apply_special_icon(self, media: Media, special_icon_file: str):
        if not special_icon_file:
            return media

        media.add_layer(
            ImageLayer.from_media_path(self.action_base.get_asset_path(special_icon_file, f"{self.ASSET_SUBDIR}/Platforms"),
                                       size=self.size, halign=self.halign, valign=self.valign)
        )

        return media

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
