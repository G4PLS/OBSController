import threading
from copy import deepcopy

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ....internal.MultiAction.MultiActionItem import MultiActionItem

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk

class SplitRecordFile(MultiActionItem):
    FIELD_NAME = "Split Record File"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.error_showing = False

        self.CUT_FILE_ERROR: Media = deepcopy(self.plugin_base.asset_manager.ERROR_ICON)
        self.CUT_FILE_ERROR.prepend_layer(ImageLayer(image=self.plugin_base.asset_manager.CUT_FILE_MEDIA))
        self.CUT_FILE_ERROR = self.CUT_FILE_ERROR.get_final_media()

    def on_update(self):
        if self.error_showing:
            return
        self.action_base.set_media(image=self.plugin_base.asset_manager.CUT_FILE_MEDIA)

    def on_tick(self):
        self.action_base.set_background_color(self.plugin_base.asset_manager.SECONDARY_BACKGROUND)

    def build_ui(self):
        self.add(Gtk.Label(label="Only in Websocket version >=5.5.0"))

    def on_key_down(self):
        status_code = self.plugin_base.backend.custom_request("SplitRecordFile")

        if status_code == "501" or status_code == "702":
            self.action_base.set_media(image=self.CUT_FILE_ERROR)
            self.error_showing = True
            threading.Timer(0.5, self.reset_error).start()

    def reset_error(self):
        self.error_showing = False
        self.on_update()