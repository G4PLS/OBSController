from src.backend.PluginManager.ActionBase import ActionBase

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ..internal.OBSConfig import OBSConfigWindow
from ..internal.PluginConfig import PluginConfigButton

class OBSAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_config = PluginConfigButton(self.plugin_base, OBSConfigWindow, True)

    def get_config_rows(self) -> "list[Adw.PreferencesRow]":
        return [self.plugin_config]