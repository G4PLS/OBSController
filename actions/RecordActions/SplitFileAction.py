import os.path
import threading

import gi

from ..OBSAction import OBSAction

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

class SplitFileAction(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_update(self):
        self.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "Record", "chapter.svg"), size=1)
        self.set_background_color([101, 124, 194, 255])

    def on_tick(self):
        self.set_background_color([101, 124, 194, 255])

    def get_custom_config_area(self):
        self.ui = super().get_custom_config_area()

        self.ui.add(Gtk.Label(label="Only in Websocket version >=5.5.0"))

        return self.ui

    #
    # ACTION
    #

    def on_key_down(self):
        status_code = self.plugin_base.backend.custom_request("SplitRecordFile")

        if status_code == "501" or status_code == "702":
            self.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "error.svg"), size=0.8)
            self.set_top_label("")
            threading.Timer(0.5, self.on_update).start()