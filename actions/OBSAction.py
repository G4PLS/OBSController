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
        self.obs_config_window = OBSConfigWindow(self.plugin_base)


    def get_config_rows(self) -> "list[Adw.PreferencesRow]":
        return [PluginConfigButton(self.plugin_base, OBSConfigWindow)]