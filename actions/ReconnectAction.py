import os.path

from src.backend.PluginManager.ActionBase import ActionBase

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from .OBSAction import OBSAction

class ReconnectAction(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_exit_started", self.obs_exit_event)

    def obs_exit_event(self, *args):
        self.update_status(self.plugin_base.backend.get_connected())

    def on_ready(self):
        self.update_status(self.plugin_base.backend.get_connected())

    def on_key_down(self):
        self.update_status(self.plugin_base.backend.reconnect())

    def update_status(self, connection_status: bool):
        if connection_status:
            self.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "OBS", "connection_established.svg"))
        else:
            self.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "OBS", "connection_lost.svg"))