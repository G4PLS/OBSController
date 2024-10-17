from ..OBSAction import OBSAction


class ReconnectAction(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_exit_started", self.obs_exit_event)

    #
    # ACTION EVENTS
    #

    def on_update(self):
        self.update_status(self.plugin_base.backend.get_connected())

    def on_key_down(self):
        self.update_status(self.plugin_base.backend.reconnect())

    def update_status(self, connection_status: bool):
        if connection_status:
            self.set_media(self.plugin_base.asset_manager.CONNECTED_MEDIA)
        else:
            self.set_media(self.plugin_base.asset_manager.DISCONNECTED_MEDIA)

    #
    # EVENTS
    #

    async def obs_exit_event(self, *args):
        self.update_status(self.plugin_base.backend.get_connected())