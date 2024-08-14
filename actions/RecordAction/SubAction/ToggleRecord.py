import gi

from .RecordActionHandler import RecordActionHandler

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

class ToggleRecord(RecordActionHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Toggle Recording", *args, **kwargs)

        self.show_pause_state = False

    def build_ui(self) -> None:
        self.show_timecode_switch = Adw.SwitchRow(title="Show Timecode")
        self.show_status_switch = Adw.SwitchRow(title="Show Record Status")
        self.show_pause_state_switch = Adw.SwitchRow(title="Show Pause State")

        self.add(self.show_timecode_switch)
        self.add(self.show_status_switch)
        self.add(self.show_pause_state_switch)

        self.connect_events()

    def connect_events(self):
        super().connect_events()

        self.show_pause_state_switch.connect("notify::active", self.pause_state_switch_changed)

    def disconnect_events(self):
        super().disconnect_events()

        try:
            self.show_pause_state_switch.disconnect_by_func(self.pause_state_switch_changed)
        except:
            pass

    def pause_state_switch_changed(self, *args):
        settings = self.action_base.get_settings()

        self.show_pause_state = self.show_pause_state_switch.get_active()
        settings["show-pause-state"] = self.show_pause_state

        self.update_button()

    def set_record_status(self, record_status):
        if not self.show_status:
            self.action_base.set_media(None)
            self.action_base.set_background_color([0, 0, 0, 0])
            return

        if record_status.get("output_active", False):
            media_file = "recording_paused.svg" \
                if (record_status.get("output_paused", False) and self.show_pause_state) \
                else "recording.svg"
            self.action_base.set_media(media_path=self.get_media_path(media_file))
            self.action_base.set_background_color([101, 124, 194, 255])
        else:
            self.action_base.set_media(media_path=self.get_media_path("not_recording.svg"))
            self.action_base.set_background_color([48, 59, 92, 255])


    def on_click(self) -> None:
        self.plugin_base.backend.toggle_record()