from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media

from ..OBSAction import OBSAction

class ReconnectAction(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_configuration = False
        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_exit_started", self.obs_exit_event)

        self.established = Media(
            size=0.95,
            layers=[
                ImageLayer.from_media_path(self.get_asset_path("obs.svg", "OBS")),
                ImageLayer.from_media_path(self.get_asset_path("connection_established.svg", "OBS"))
            ]
        ).get_final_media()
        self.lost = Media(
            size=0.95,
            layers=[
                ImageLayer.from_media_path(self.get_asset_path("obs.svg", "OBS")),
                ImageLayer.from_media_path(self.get_asset_path("connection_lost.svg", "OBS"))
            ]
        ).get_final_media()

    def obs_exit_event(self, *args):
        self.update_status(self.plugin_base.backend.get_connected())

    def on_ready(self):
        super().on_ready()

        self.update_status(self.plugin_base.backend.get_connected())

    def on_key_down(self):
        self.update_status(self.plugin_base.backend.reconnect())

    def update_status(self, connection_status: bool):
        if connection_status:
            self.set_media(image=self.established)
        else:
            self.set_media(image=self.lost)