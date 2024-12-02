from gi.repository import Adw

from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.PluginManager.PluginSettings.Asset import Color


class OBSAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True

        self.plugin_base.asset_manager.colors.add_listener(self.color_changed)
        self.plugin_base.asset_manager.icons.add_listener(self.icon_changed)

    async def color_changed(self, event, key, asset: Color):
        pass

    async def icon_changed(self, event, key, asset):
        pass

    def get_custom_config_area(self):
        self.ui = Adw.PreferencesGroup()
        return self.ui