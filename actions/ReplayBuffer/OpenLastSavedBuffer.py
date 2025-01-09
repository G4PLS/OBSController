import subprocess

from src.backend.DeckManagement.InputIdentifier import InputEvent, Input
from src.backend.PluginManager.ActionBase import ActionBase
#from src.backend.Logging.Loggers.PluginLogger import plugin_logger
from GtkHelper.GtkHelper import better_disconnect
from ...globals import Icons, Colors
import gi

from ...internal.helper import run_command_detached

from GtkHelper.SearchComboRow import SearchComboRow

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ..OBSAction import OBSAction

class OpenLastSavedBuffer(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon_keys = [Icons.SAVE_BUFFER]
        self.color_keys = [Colors.SECONDARY]

        self._icon_name = Icons.OPEN_BUFFER
        self._color_name = Colors.SECONDARY

        self._current_icon = self.get_icon(self._icon_name)
        self._current_color = self.get_color(self._color_name)

    # Action Events

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        self.show_icon()
        self.show_label()
        self.show_color()

    def on_short_up(self):
        status = self.plugin_base.backend.get_last_replay_buffer_replay()

        if not status:
            return

        replay_path = status.get("saved_replay_path", None)

        if replay_path:
            run_command_detached(["xdg-open", replay_path])

    # Ui Definition

    def get_custom_config_area(self):
        pass

    # Setting Loaders

    # Ui Events

    # Displaying

    # Asset Managing

    # Misc