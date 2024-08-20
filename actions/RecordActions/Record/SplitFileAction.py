import os.path
import threading

import gi

from ...ActionHandler import ActionHandler

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

class SplitFileAction(ActionHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.build_ui()

    def on_update(self):
        self.action_base.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "Record", "cut_record_file.svg"), size=1)
        self.action_base.set_background_color(self.plugin_base.PRIMARY_BACKGROUND)

    def on_tick(self):
        self.action_base.set_media(self.action_base.get_asset_path("cut_record_file.svg", subdir="Record"))
        self.action_base.set_background_color(self.plugin_base.PRIMARY_BACKGROUND)

    def build_ui(self) -> None:
        self.add(Gtk.Label(label="Only in Websocket version >=5.5.0"))

    #
    # ACTION
    #

    def on_key_down(self):
        status_code = self.plugin_base.backend.custom_request("SplitRecordFile")

        if status_code == "501" or status_code == "702":
            self.action_base.set_media(media_path=os.path.join(self.plugin_base.PATH, "assets", "error.svg"), size=0.8)
            self.action_base.set_top_label("")
            threading.Timer(0.5, self.on_update).start()