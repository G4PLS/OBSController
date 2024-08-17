import os

import gi

from ..ActionHandler import ActionHandler

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw


class StreamActionHandler(ActionHandler):
    ASSET_SUBDIR = "Stream"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_status: bool = False

        self.current_image: str = ""

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_record_state_changed",
                                                  self.stream_state_changed)

    def on_ready(self) -> None:
        self.load_settings()

    def on_update(self) -> None:
        self.update_button()

    def build_ui(self) -> None:
        self.show_status_switch = Adw.SwitchRow(title="Show Stream Status")

        self.add(self.show_status_switch)

    def connect_events(self):
        self.show_status_switch.connect("notify::active", self.status_switch_changed)

    def disconnect_events(self):
        try:
            self.show_status_switch.disconnect_by_func(self.status_switch_changed)
        except:
            pass

    def status_switch_changed(self, *args):
        settings = self.action_base.get_settings()

        self.show_status = self.show_status_switch.get_active()
        settings["show-status"] = self.show_status

        self.action_base.set_settings(settings)

        self.update_button()

    def load_settings(self):
        settings = self.action_base.get_settings()

        self.show_status = settings.get("show-status", False)

    def load_ui_settings(self):
        self.disconnect_events()

        self.show_status_switch.set_active(self.show_status)

        self.connect_events()

    async def stream_state_changed(self, event_id: str, obs_event: str, message: dict):
        self.update_button()

    def update_button(self):
        print("STREAM ACTION HANDLER")
        status = self.plugin_base.backend.get_stream_status()

        if status is None:
            self.show_error()
            return

        self.set_stream_status(status)

    def on_tick(self):
        self.update_button()

    def set_stream_status(self, stream_status):
        pass

    def update_status_image(self, new_image, subdir_override: str = None):
        if not subdir_override:
            subdir_override = self.ASSET_SUBDIR

        if new_image != self.current_image:
            self.current_image = new_image
            self.action_base.set_media(
                media_path=self.get_media_path(self.current_image, subdir=subdir_override),
                size=1,
                update=True)
        self.action_base.set_media(
            media_path=self.get_media_path(self.current_image, subdir=subdir_override),
            size=1,
            update=False)

    def get_media_path(self, asset_name: str, subdir: str = None) -> str:
        if subdir:
            return os.path.join(self.plugin_base.PATH, "assets", subdir, asset_name)
        else:
            return os.path.join(self.plugin_base.PATH, "assets", asset_name)

    def show_error(self):
        self.action_base.set_media(media_path=self.get_media_path("connection_lost.svg", "OBS"), size=0.75)
        self.action_base.set_background_color([82, 101, 158, 255])