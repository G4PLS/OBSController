import threading
from copy import deepcopy

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ...OBSMultiActionItem import OBSMultiActionItem
from ....globals import Icons
from ....internal.MultiAction.MultiActionItem import MultiActionItem

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk

class SplitRecordFile(OBSMultiActionItem):
    FIELD_NAME = "Split Record File"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Action Events

    def on_update(self):
        self.action_base.set_background_color(self.secondary_color)

        _, render = self.plugin_base.asset_manager.icons.get_asset_values(Icons.REC_SPLIT)
        self.action_base.set_media(image=render)

    def on_key_down(self):
        status_code = self.plugin_base.backend.custom_request("SplitRecordFile")

        if status_code == "501" or status_code == "702":
            pass

    # Asyncs

    async def icon_changed(self, event: str, key: str, asset):
        if key in [Icons.REC_SPLIT]:
            self.on_update()

    def color_changed(self):
        self.on_update()

    # UI

    def build_ui(self):
        self.add(Gtk.Label(label="Only in Websocket version >=5.5.0"))