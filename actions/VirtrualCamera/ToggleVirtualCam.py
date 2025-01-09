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

class ToggleVirtualCam(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_pause_state: bool = False
        self.show_timecode: bool = False
        self.recording_offset: int = 0
        self.timecode_location: str = "top"

        self.icon_keys = [Icons.VIRTUAL_CAM_ON, Icons.VIRTUAL_CAM_OFF]
        self.color_keys = [Colors.PRIMARY, Colors.SECONDARY]

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_virtualcam_state_changed",
                                                  self.cam_state_changed)


    # Action Events

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        self.change_icon({})
        self.change_color({})

        self.show_icon()
        self.show_label()
        self.show_color()

    def on_tick(self):
        status = self.plugin_base.backend.get_virtual_cam_status() or {}
        self.change_icon(status)
        self.change_color(status)

        self.show_icon()
        self.show_label()
        self.show_color()

    def on_short_up(self):
        self.plugin_base.backend.toggle_virtual_cam()

    # Ui Definition

    def get_custom_config_area(self):
        pass

    # Setting Loaders

    # Ui Events

    # Displaying

    def change_color(self, status):
        if status.get("output_active", False):
            self._color_name = Colors.PRIMARY
        else:
            self._color_name = Colors.SECONDARY
        self._current_color = self.get_color(self._color_name)

    def change_icon(self, status):
        if status.get("output_active", False):
            self._icon_name = Icons.VIRTUAL_CAM_ON
        else:
            self._icon_name = Icons.VIRTUAL_CAM_OFF
        self._current_icon = self.get_icon(self._icon_name)

    # Asset Managing

    async def cam_state_changed(self, event_id: str, obs_event: str, message: dict):
        self.change_icon(message)
        self.change_color(message)

        self.show_icon()
        self.show_color()

    # Misc