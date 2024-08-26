from src.backend.DeckManagement.Subclasses.ImageLayer import ImageLayer

from ..OBSAction import OBSAction

class ReconnectAction(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_exit_started", self.obs_exit_event)

        self.obs_layer = ImageLayer.from_media_path(self.get_asset_path("obs.svg", "OBS"))
        self.established_image = ImageLayer.to_layered_image([
            self.obs_layer,
            ImageLayer.from_media_path(media_path=self.get_asset_path("connection_established.svg", "OBS"))
        ])
        self.lost_image = ImageLayer.to_layered_image([
            self.obs_layer,
            ImageLayer.from_media_path(self.get_asset_path("connection_lost.svg", "OBS"))
        ])

    def obs_exit_event(self, *args):
        self.update_status(self.plugin_base.backend.get_connected())

    def on_ready(self):
        self.update_status(self.plugin_base.backend.get_connected())

    def on_key_down(self):
        self.update_status(self.plugin_base.backend.reconnect())

    def update_status(self, connection_status: bool):
        if connection_status:
            self.set_media(image=self.established_image)
        else:
            self.set_media(image=self.lost_image)