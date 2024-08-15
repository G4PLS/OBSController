import os.path

import gi
from ...ActionHandler import ActionHandler

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

class RecordActionHandler(ActionHandler):
    ASSET_SUBDIR = "Record"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_timecode: bool = False
        self.show_status: bool = False

        self.current_image: str = ""
        self.display_error: bool = False

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_record_state_changed", self.record_state_changed)
        self.plugin_base.connect_to_event("com.gapls.OBSController::RecordStatusEvent", self.record_status_update)

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

    async def record_state_changed(self, event_id: str, obs_event: str, message: dict):
        self.update_button()

    async def record_status_update(self, event_id: str, status):
        self.set_record_status(status)

    def update_button(self):
        status = self.plugin_base.backend.get_record_status()

        if status is None:
            self.show_error()
            return

        self.set_record_status(status)
        self.set_timecode(status)

    def on_tick(self):
        self.update_button()

    def set_record_status(self, record_status):
        if not self.show_status or not record_status:
            self.action_base.set_media(None)
            self.action_base.set_background_color([0, 0, 0, 0])
            return

        new_image = ""

        if record_status.get("output_active", False):
            new_image = "recording_paused.svg" if record_status.get("output_paused", False) else "recording.svg"
            self.action_base.set_background_color([101, 124, 194, 255])
        else:
            new_image = "not_recording.svg"
            self.action_base.set_background_color([48, 59, 92, 255])

        self.update_status_image(new_image)

    def update_status_image(self, new_image):
        if new_image != self.current_image:
            self.current_image = new_image
            self.action_base.set_media(
                media_path=self.get_media_path(self.current_image, subdir=self.ASSET_SUBDIR),
                size=1,
                update=True)
        self.action_base.set_media(
            media_path=self.get_media_path(self.current_image, subdir=self.ASSET_SUBDIR),
            size=1,
            update=False)

    def set_timecode(self, record_status):
        if self.show_timecode:
            timecode = record_status.get("output_timecode", "00:00:00.000")
            timecode = timecode.split(".")[0]

            self.action_base.set_top_label(timecode)
        else:
            self.action_base.set_top_label("")

    def get_media_path(self, asset_name: str, subdir: str = None) -> str:
        if subdir:
            return os.path.join(self.plugin_base.PATH, "assets", subdir, asset_name)
        else:
            return os.path.join(self.plugin_base.PATH, "assets", asset_name)

    def show_error(self):
        self.action_base.set_media(media_path=self.get_media_path("connection_lost.svg"), size=0.75)