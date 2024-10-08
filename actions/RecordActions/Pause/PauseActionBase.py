import gi

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ..RecordActionHandler import RecordActionHandler

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

class PauseActionBase(RecordActionHandler):
    """
        Used for actual sub-actions specialized for Pausing the Recording
        """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.update_with_obs: bool = False

        self.PAUSED = Media(layers=[
            ImageLayer.from_media_path(self.get_media_path("recording_rings_on.svg", "Record/Rings")),
            ImageLayer.from_media_path(self.get_media_path("little_pause_on.svg", "Record/Pause"))
        ]).get_final_media()

        self.UNPAUSED = Media(layers=[
            ImageLayer.from_media_path(self.get_media_path("recording_rings_off.svg", "Record/Rings")),
            ImageLayer.from_media_path(self.get_media_path("little_pause_off.svg", "Record/Pause"))
        ]).get_final_media()

    def build_ui(self) -> None:
        self.show_status_switch = Adw.SwitchRow(title="Show Pause Status")

        self.update_with_obs_switch = Adw.SwitchRow(title="Update Pause State with OBS",
                                                    tooltip_text="When this is active the button will change the Icon based on the current paused state in obs")

        self.add(self.show_status_switch)
        self.add(self.update_with_obs_switch)

        self.connect_events()

    def connect_events(self):
        super().connect_events()

        self.update_with_obs_switch.connect("notify::active", self.update_obs_switch_changed)

    def disconnect_events(self):
        super().disconnect_events()

        try:
            self.update_with_obs_switch.disconnect_by_func(self.update_obs_switch_changed)
        except:
            pass

    def update_obs_switch_changed(self, *args):
        settings = self.action_base.get_settings()

        self.update_with_obs = self.update_with_obs_switch.get_active()

        settings["update-pause-obs"] = self.update_with_obs
        self.action_base.set_settings(settings)

    def load_settings(self):
        super().load_settings()

        settings = self.action_base.get_settings()

        self.update_with_obs = settings.get("update-pause-obs", False)

    def load_ui_settings(self):
        super().load_ui_settings()

        self.disconnect_events()

        self.update_with_obs_switch.set_active(self.update_with_obs)

        self.connect_events()

    async def record_state_changed(self, event_id: str, obs_event: str, message: dict):
        if not self.update_with_obs_switch:
            return

        self.update_button()

    async def record_status_update(self, event_id: str, status):
        if not self.update_with_obs_switch:
            return

        self.set_record_status(status)

    def set_record_status(self, record_status):
        if not self.show_status:
            self.action_base.set_media(None)
            self.action_base.set_background_color([0, 0, 0, 0])
            return

        paused = record_status.get("output_paused", False)

        if paused or not self.update_with_obs:
            self.action_base.set_background_color(self.plugin_base.PRIMARY_BACKGROUND)
            new_image = self.PAUSED
        else:
            self.action_base.set_background_color(self.plugin_base.SECONDARY_BACKGROUND)
            new_image = self.UNPAUSED

        self.update_status_image(new_image)