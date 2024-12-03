from src.backend.PluginManager.PluginSettings.Asset import Color, Icon
from ..OBSAction import OBSAction


class ReconnectAction(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_exit_started", self.obs_exit_event)

    async def icon_changed(self, event, key, asset: Icon):
        if key == "connected" or key == "disconnected":
            self.update_status(self.plugin_base.backend.get_connected())

    def color_changed(self):
        self.set_background_color(self.secondary_color)

    #
    # ACTION EVENTS
    #

    def on_update(self):
        self.update_status(self.plugin_base.backend.get_connected())

        color = self.plugin_base.asset_manager.colors.get_asset_values("secondary")
        self.set_background_color(list(color))

    def on_key_down(self):
        self.update_status(self.plugin_base.backend.reconnect())

    def update_status(self, connection_status: bool):
        if connection_status:
            _, render = self.plugin_base.asset_manager.icons.get_asset_values("connected")
        else:
            _, render = self.plugin_base.asset_manager.icons.get_asset_values("disconnected")

        if render:
            self.set_media(image=render)

    #
    # EVENTS
    #

    async def obs_exit_event(self, *args):
        self.update_status(self.plugin_base.backend.get_connected())