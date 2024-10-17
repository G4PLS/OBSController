import threading
from copy import deepcopy
from sqlite3 import connect

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ....internal.ComboAction.ComboActionRow import ComboActionItem, ComboActionRow
from ....internal.MultiAction.MultiActionItem import MultiActionItem

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import rpyc
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

class AddRecordChapter(MultiActionItem):
    FIELD_NAME = "Add Record Chapter"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chapter_name: str = ""
        self.location_index: int = 0

        self.error_showing = False

        self.CHAPTER_ERROR: Media = deepcopy(self.plugin_base.asset_manager.ERROR_ICON)
        self.CHAPTER_ERROR.prepend_layer(ImageLayer(image=self.plugin_base.asset_manager.RECORD_CHAPTER_MEDIA))
        self.CHAPTER_ERROR = self.CHAPTER_ERROR.get_final_media()

        self.location_items = [
            ComboActionItem(name="Top", callback=self.action_base.set_top_label),
            ComboActionItem(name="Center", callback=self.action_base.set_center_label),
            ComboActionItem(name="Bottom", callback=self.action_base.set_bottom_label)
        ]

    #
    # UI
    #

    def build_ui(self):
        self.chapter_location = ComboActionRow(title="Chapter Name Location")
        self.chapter_name_entry = Adw.EntryRow(title="Record Chapter Name")

        self.add(self.chapter_location)
        self.add(self.chapter_name_entry)
        self.add(Gtk.Label(label="Only in Websocket version >=5.5.0 and only with Hybrid MP4"))

    #
    # UI EVENTS
    #

    def connect_events(self):
        self.chapter_location.connect("item-changed", self.chapter_location_changed)
        self.chapter_name_entry.connect("changed", self.chapter_name_changed)

    def disconnect_events(self):
        try:
            self.chapter_location.disconnect_by_func(self.chapter_location_changed)
            self.chapter_name_entry.disconnect_by_func(self.chapter_name_changed)
        except:
            pass

    def chapter_location_changed(self, object, item, index):
        settings = self.get_settings()

        self.location_items[self.location_index].callback("")

        self.location_index = index
        settings["chapter-location"] = self.location_index

        self.display_chapter_label()

        self.set_settings(settings)

    def chapter_name_changed(self, *args):
        settings = self.get_settings()

        self.chapter_name = self.chapter_name_entry.get_text()

        self.display_chapter_label()

        settings["chapter-name"] = self.chapter_name
        self.set_settings(settings)

    #
    # ACTION EVENTS
    #

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        if self.error_showing:
            return
        self.display_chapter_label()
        self.action_base.set_media(image=self.plugin_base.asset_manager.RECORD_CHAPTER_MEDIA)

    def on_tick(self):
        self.action_base.set_background_color(self.plugin_base.asset_manager.SECONDARY_BACKGROUND)

    def on_key_down(self):
        if not self.chapter_name:
            return

        status_code = self.plugin_base.backend.custom_request("CreateRecordChapter", {"chapterName": self.chapter_name})

        if status_code == "501" or status_code == "702":
            self.action_base.set_media(image=self.CHAPTER_ERROR)
            threading.Timer(0.5, self.reset_error).start()

    #
    # SETTINGS
    #

    def load_settings(self):
        settings = self.get_settings()

        self.location_index = settings.get("chapter-location", 0)
        self.chapter_name = settings.get("chapter-name", None)

        self.display_chapter_label()

    def load_ui_settings(self):
        self.disconnect_events()

        self.chapter_name_entry.set_text(self.chapter_name or "")
        self.chapter_location.set_model_items(self.location_items, self.location_index)

        self.connect_events()

    #
    #
    # MISC

    def display_chapter_label(self):
        if not self.chapter_name:
            self.chapter_name = ""

        if self.location_items[self.location_index].callback:
            self.location_items[self.location_index].callback(self.chapter_name)
        else:
            self.action_base.set_top_label(self.chapter_name)

    def reset_error(self):
        self.error_showing = False
        self.on_update()