from src.backend.PluginManager.PluginSettings.Asset import Icon, Color
from data.plugins.com_gapls_OBSController.internal.MultiAction import MultiActionItem

from ..globals import Colors

class OBSMultiActionItem(MultiActionItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_base.asset_manager.icons.add_listener(self.icon_changed)
        self.plugin_base.asset_manager.colors.add_listener(self._color_changed)

        self.primary_color = self.plugin_base.asset_manager.colors.get_asset_values(Colors.PRIMARY)
        self.secondary_color = self.plugin_base.asset_manager.colors.get_asset_values(Colors.SECONDARY)

    def on_update(self):
        self.display_icon({})

    def display_icon(self, status):
        pass

    async def icon_changed(self, event: str, key: str, asset: Icon):
        pass

    async def _color_changed(self, event: str, key: str, asset: Color):
        if key == Colors.PRIMARY:
            self.primary_color = asset.get_values()
        elif key == Colors.SECONDARY:
            self.secondary_color = asset.get_values()

        self.color_changed()

    def color_changed(self):
        pass