from gi.repository import Adw

from data.plugins.com_gapls_OBSController.globals import Colors
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.PluginManager.PluginSettings.Asset import Color


class OBSAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True

        self.primary_color = self.plugin_base.asset_manager.colors.get_asset_values(Colors.PRIMARY)
        self.secondary_color = self.plugin_base.asset_manager.colors.get_asset_values(Colors.SECONDARY)

        self.plugin_base.asset_manager.colors.add_listener(self._color_changed)
        self.plugin_base.asset_manager.icons.add_listener(self.icon_changed)

    def on_update(self):
        self.display_icon({})

    async def _color_changed(self, event: str, key: str, asset: Color):
        if key == Colors.PRIMARY:
            self.primary_color = asset.get_values()
        elif key == Colors.SECONDARY:
            self.secondary_color = asset.get_values()

        self.color_changed()

    async def icon_changed(self, event, key, asset):
        pass

    def color_changed(self):
        pass

    def get_custom_config_area(self):
        self.ui = Adw.PreferencesGroup()
        return self.ui

    def display_icon(self, status):
        pass