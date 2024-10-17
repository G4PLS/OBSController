import threading

import gi

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ...ActionHandler import ActionHandler

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

import rpyc



class RecordChapter(ActionHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Record Chapter", *args, **kwargs)

        self.chapter_name = None

        self.CHAPTER = ImageLayer.from_media_path(media_path=self.action_base.get_asset_path("chapter.svg", "Record"))

        self.ERROR = Media(layers=[
            self.CHAPTER,
            ImageLayer.from_media_path(media_path=self.action_base.get_asset_path("error.svg", "OBS"), size=0.75)
        ]).get_final_media()

        self.build_ui()

    def on_ready(self):
        self.load_settings()

    def build_ui(self) -> None:
        self.chapter_name_entry = Adw.EntryRow(title="Record Chapter Name")

        self.add(self.chapter_name_entry)
        self.add(Gtk.Label(label="Only in Websocket version >=5.5.0 and only with Hybrid MP4"))

        self.load_ui_settings()

        self.connect_events()

    def on_update(self):
        self.action_base.set_media(image=self.CHAPTER.image)
        self.action_base.set_background_color(self.plugin_base.PRIMARY_BACKGROUND)
        self.set_chapter_label()

    def on_tick(self):
        self.action_base.set_media(image=self.CHAPTER.image)
        self.action_base.set_background_color(self.plugin_base.PRIMARY_BACKGROUND)
        self.set_chapter_label()

    #
    # EVENTS
    #

    def connect_events(self):
        self.chapter_name_entry.connect("changed", self.chapter_name_changed)

    def disconnect_events(self):
        try:
            self.chapter_name_entry.disconnect_by_func(self.chapter_name_changed)
        except:
            pass

    def chapter_name_changed(self, *args):
        settings: dict = self.action_base.get_settings()

        self.chapter_name = self.chapter_name_entry.get_text()

        self.set_chapter_label()

        if len(self.chapter_name) != 0:
            settings["chapter-name"] = self.chapter_name
        elif settings.__contains__("chapter-name"):
            settings.pop("chapter-name")
        self.action_base.set_settings(settings)

    #
    # SETTINGS
    #

    def load_ui_settings(self):
        self.disconnect_events()

        self.chapter_name_entry.set_text(self.chapter_name or "")

        self.connect_events()

    def load_settings(self):
        settings = self.action_base.get_settings()

        self.chapter_name = settings.get("chapter-name", None)

        self.on_update()

    def set_chapter_label(self):
        if self.chapter_name is not None:
            self.action_base.set_top_label(self.chapter_name)
        else:
            self.action_base.set_top_label("")

    #
    # ACTION
    #

    def on_click(self):
        if not self.chapter_name:
            return

        status_code = self.plugin_base.backend.custom_request("CreateRecordChapter", {"chapterName": self.chapter_name})

        if status_code == "501" or status_code == "702":
            self.action_base.set_media(image=self.ERROR)
            self.action_base.set_top_label("")
            threading.Timer(0.5, self.on_update).start()