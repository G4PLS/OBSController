import gi
from src.backend.PluginManager.ActionBase import ActionBase

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

from ..internal.OBSConfig import OBSConfigWindow
from ..internal.PluginConfig import PluginConfigButton

class OBSAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_config = PluginConfigButton(self.plugin_base, OBSConfigWindow, True)

    def get_custom_config_area(self):
        self.ui = Adw.PreferencesGroup()
        self.ui.add(self.plugin_config)

        return self.ui