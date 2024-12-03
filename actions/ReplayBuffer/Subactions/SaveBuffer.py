import threading
from copy import deepcopy

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ...OBSMultiActionItem import OBSMultiActionItem
from ....globals import Icons
from ....internal.MultiAction.MultiActionItem import MultiActionItem
from ....internal.ComboAction.ComboActionRow import ComboActionRow, ComboActionItem
from ....internal.DuoPreferencesRow import DuoPreferencesRow

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class SaveBuffer(OBSMultiActionItem):
    FIELD_NAME = "Save Buffer"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #
    # ACTION EVENTS
    #

    def on_update(self):
        self.action_base.set_background_color(self.secondary_color)

        _, render = self.plugin_base.asset_manager.icons.get_asset_values(Icons.SAVE_BUFFER)
        self.action_base.set_media(image=render)

    def on_key_down(self):
        self.plugin_base.backend.save_replay_buffer()

    # Asyncs

    async def icon_changed(self, event: str, key: str, asset):
        if key in [Icons.SAVE_BUFFER]:
            self.on_update()

    def color_changed(self):
        self.on_update()

    #
    # MISC
    #