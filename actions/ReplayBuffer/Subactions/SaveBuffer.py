import threading
from copy import deepcopy

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ....internal.MultiAction.MultiActionItem import MultiActionItem
from ....internal.ComboAction.ComboActionRow import ComboActionRow, ComboActionItem
from ....internal.DuoPreferencesRow import DuoPreferencesRow

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class SaveBuffer(MultiActionItem):
    FIELD_NAME = "Save Buffer"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.REPLAY_SAVED: Media = deepcopy(self.plugin_base.asset_manager.SAVE_BUFFER_ICON)
        self.REPLAY_SAVED.append_layer(ImageLayer(image=self.plugin_base.asset_manager.SUCCESS_MEDIA))
        self.REPLAY_SAVED = self.REPLAY_SAVED.get_final_media()

        self.success_showing = False

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_replay_buffer_saved",
                                                  self.buffer_saved)

    #
    # ACTION EVENTS
    #

    def on_update(self):
        if self.success_showing:
            return

        self.action_base.set_media(self.plugin_base.asset_manager.SAVE_BUFFER_MEDIA)

    def on_tick(self):
        self.action_base.set_background_color(self.plugin_base.asset_manager.SECONDARY_BACKGROUND)

    def on_key_down(self):
        self.plugin_base.backend.save_replay_buffer()

    #
    # MISC
    #

    async def buffer_saved(self, *args):
        self.action_base.set_media(image=self.REPLAY_SAVED)
        self.success_showing = True
        threading.Timer(0.5, self.reset_success).start()

    def reset_success(self):
        self.success_showing = False
        self.on_update()