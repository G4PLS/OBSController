import os.path

import gi

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ..ActionHandler import ActionHandler

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

class RecordActionHandler(ActionHandler):
    """
    Base for the Record Sub-Actions, adding default behaviour and variables to make record actions easier to define
    """

    ASSET_SUBDIR = "Record"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_status: bool = True

        self.current_image: str = ""
        self.display_error: bool = False

        self.connection_lost_layer = Media(layers=[
            ImageLayer.from_media_path(self.get_media_path(asset_name="obs.svg", subdir="OBS")),
            ImageLayer.from_media_path(self.get_media_path(asset_name="connection_lost.svg", subdir="OBS"))
        ]).get_final_media()

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_record_state_changed", self.record_state_changed)

        self.build_ui()

    def on_ready(self) -> None:
        self.load_settings()

    def on_update(self) -> None:
        self.update_button()

    def build_ui(self) -> None:
        self.show_status_switch = Adw.SwitchRow(title="Show Record Status")

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

        self.show_status = settings.get("show-status", True)

    def load_ui_settings(self):
        self.disconnect_events()

        self.show_status_switch.set_active(self.show_status)

        self.connect_events()

    async def record_state_changed(self, event_id: str, obs_event: str, message: dict):
        self.update_button()

    def update_button(self):
        status = self.plugin_base.backend.get_record_status()

        if status is None:
            self.show_error()
            return

        self.set_record_status(status)

    def on_tick(self):
        self.update_button()

    def set_record_status(self, record_status):
        pass

    def update_status_image(self, new_image):
        if new_image != self.current_image:
            self.current_image = new_image
            self.action_base.set_media(
                image=self.current_image,
                size=1,
                update=True)
        self.action_base.set_media(
            image=self.current_image,
            size=1,
            update=False)

    def get_media_path(self, asset_name: str, subdir: str = None) -> str:
        if subdir:
            return os.path.join(self.plugin_base.PATH, "assets", subdir, asset_name)
        else:
            return os.path.join(self.plugin_base.PATH, "assets", asset_name)

    def show_error(self):
        self.action_base.set_media(self.connection_lost_layer)
        self.action_base.set_background_color([82, 101, 158, 255])