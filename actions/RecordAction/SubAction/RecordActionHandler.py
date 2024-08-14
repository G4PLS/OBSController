import os.path

from plugins.OBSController.actions.ActionHandler import ActionHandler

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class RecordActionHandler(ActionHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_timecode: bool = False
        self.show_status: bool = False

        self.recording = False

        self.plugin_base.connect_to_event("com.gapls.OBSController::OBSEvent", "on_record_state_changed", self.record_state_changed)

    def on_ready(self) -> None:
        self.update_button()

    def build_ui(self) -> None:
        self.show_timecode_switch = Adw.SwitchRow(title="Show Timecode")
        self.show_status_switch = Adw.SwitchRow(title="Show Record Status")

        self.add(self.show_timecode_switch)
        self.add(self.show_status_switch)

        self.connect_events()

    def connect_events(self):
        self.show_timecode_switch.connect("notify::active", self.timecode_switch_changed)
        self.show_status_switch.connect("notify::active", self.status_switch_changed)

    def disconnect_events(self):
        try:
            self.show_timecode_switch.disconnect_by_func(self.timecode_switch_changed)
            self.show_status_switch.disconnect_by_func(self.status_switch_changed)
        except:
            pass

    def timecode_switch_changed(self, *args):
        settings = self.action_base.get_settings()

        self.show_timecode = self.show_timecode_switch.get_active()
        settings["show-timecode"] = self.show_timecode

        self.action_base.set_settings(settings)

        self.update_button()

    def status_switch_changed(self, *args):
        settings = self.action_base.get_settings()

        self.show_status = self.show_status_switch.get_active()
        settings["show-status"] = self.show_status

        self.action_base.set_settings(settings)

        self.update_button()

    def load_settings(self):
        settings = self.action_base.get_settings()

        self.show_timecode = settings.get("show-timecode", False)
        self.show_status = settings.get("show-status", False)

    def load_ui_settings(self):
        self.disconnect_events()

        self.show_timecode_switch.set_active(self.show_timecode)
        self.show_status_switch.set_active(self.show_status)

        self.connect_events()

    def on_tick(self) -> None:
        self.update_button()

    async def record_state_changed(self, event_id: str, obs_event: str, message: dict):
        self.update_button()

    def update_button(self):
        status = self.plugin_base.backend.get_record_status()

        if status is None:
            self.action_base.show_error(0.5)
            return

        self.set_record_status(status)
        self.set_timecode(status)

    def set_record_status(self, record_status):
        if not self.show_status:
            self.action_base.set_media(None)
            self.action_base.set_background_color([0, 0, 0, 0])
            return

        if record_status.get("output_active", False):
            media_file = "recording_paused.svg" if record_status.get("output_paused", False) else "recording.svg"
            self.action_base.set_media(media_path=self.get_media_path(media_file))
            self.action_base.set_background_color([101, 124, 194, 255])
        else:
            self.action_base.set_media(media_path=self.get_media_path("not_recording.svg"))
            self.action_base.set_background_color([48, 59, 92, 255])

    def set_timecode(self, record_status):
        if self.show_timecode:
            timecode = record_status.get("output_timecode", "00:00:00.000")
            timecode = timecode.split(".")[0]

            self.action_base.set_top_label(timecode)
        else:
            self.action_base.set_top_label("")

    def get_media_path(self, asset_name: str) -> str:
        return os.path.join(self.plugin_base.PATH, "assets", "Record", asset_name)