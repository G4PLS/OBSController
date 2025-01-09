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

from loguru import logger as log

from ..OBSAction import OBSAction

class SplitRecordFile(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_configuration = False

        self.icon_keys = [Icons.REC_SPLIT]
        self.color_keys = [Colors.SECONDARY]

        self._icon_name = Icons.REC_SPLIT
        self._color_name = Colors.SECONDARY

        self._current_icon = self.get_icon(self._icon_name)
        self._current_color = self.get_color(self._color_name)

    # Action Events

    def on_update(self):
        self.show_icon()
        self.show_color()

    def on_short_up(self):
        status_code = self.plugin_base.backend.custom_request("SplitRecordFile")

        if status_code == "501" or status_code == "702":
            log.warning(f"SPLIT RECORD FILE RETURNED: {status_code}")

    # Ui Definition

    def get_custom_config_area(self):
        pass

    # Setting Loaders

    # Ui Events

    # Displaying

    # Asset Managing

    # Misc
