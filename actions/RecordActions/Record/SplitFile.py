import threading

import gi

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ...ActionHandler import ActionHandler

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk

class SplitFile(ActionHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.CUT_FILE = ImageLayer.from_media_path(media_path=self.action_base.get_asset_path("cut_record_file.svg", "Record"))

        self.ERROR = Media(layers=[
            self.CUT_FILE,
            ImageLayer.from_media_path(media_path=self.action_base.get_asset_path("error.svg", "OBS"), size=0.75)
            ]).get_final_media()

        self.build_ui()

    def on_update(self):
        self.action_base.set_media(image=self.CUT_FILE.image)
        self.action_base.set_background_color(self.plugin_base.PRIMARY_BACKGROUND)

    def on_tick(self):
        self.action_base.set_media(image=self.CUT_FILE.image)
        self.action_base.set_background_color(self.plugin_base.PRIMARY_BACKGROUND)

    def build_ui(self) -> None:
        self.add(Gtk.Label(label="Only in Websocket version >=5.5.0"))

    #
    # ACTION
    #

    def on_click(self):
        status_code = self.plugin_base.backend.custom_request("SplitRecordFile")

        if status_code == "501" or status_code == "702":
            self.action_base.set_media(image=self.ERROR)
            self.action_base.set_top_label("")
            threading.Timer(0.5, self.on_update).start()