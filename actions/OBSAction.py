from gi.repository import Adw

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from src.backend.PluginManager.ActionBase import ActionBase
from ..internal.MultiAction.MultiAction import MultiAction
from ..internal.PluginConfig import PluginConfigButton
from ..internal.OBSConfig import OBSConfigWindow


class OBSAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_config = PluginConfigButton(self.plugin_base, OBSConfigWindow, True)
        self.has_configuration = True
        self.obs_config_setup = False

    def on_ready(self):
        plugin_settings = self.plugin_base.get_settings()
        self.obs_config_setup = plugin_settings.get("first-setup", False)

    def get_custom_config_area(self):
        self.ui = Adw.PreferencesGroup()

        self.plugin_config.unparent()
        self.ui.add(self.plugin_config)

        if not self.obs_config_setup:
            self.plugin_config.open_config_window()
            self.obs_config_setup = True

            plugin_settings = self.plugin_base.get_settings()
            plugin_settings["first-setup"] = self.obs_config_setup
            self.plugin_base.set_settings(plugin_settings)

        return self.ui