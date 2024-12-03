import threading
from copy import deepcopy
from sqlite3 import connect

from GtkHelper.GtkHelper import better_disconnect
from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ...OBSMultiActionItem import OBSMultiActionItem
from ....globals import Icons
from ....internal.ComboAction.ComboActionRow import ComboActionItem, ComboActionRow
from ....internal.MultiAction.MultiActionItem import MultiActionItem

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import rpyc
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

class AddRecordChapter(OBSMultiActionItem):
    FIELD_NAME = "Add Record Chapter"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chapter_name: str = ""
        self.location_index: int = 0

        self.location_items = [
            ComboActionItem(name="Top", callback=self.action_base.set_top_label),
            ComboActionItem(name="Center", callback=self.action_base.set_center_label),
            ComboActionItem(name="Bottom", callback=self.action_base.set_bottom_label)
        ]

    # Action Events

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        self.action_base.set_background_color(self.secondary_color)

        self.display_chapter_label()

        _, render = self.plugin_base.asset_manager.icons.get_asset_values(Icons.REC_CHAPTER)
        self.action_base.set_media(image=render)

    def on_key_down(self):
        if not self.chapter_name:
            return

        status_code = self.plugin_base.backend.custom_request("CreateRecordChapter", {"chapterName": self.chapter_name})

        if status_code == "501" or status_code == "702":
            pass

    # Asyncs

    async def icon_changed(self, event: str, key: str, asset):
        if key in [Icons.REC_CHAPTER]:
            self.on_update()

    def color_changed(self):
        self.on_update()

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
        better_disconnect(self.chapter_location, self.chapter_location_changed)
        better_disconnect(self.chapter_name_entry, self.chapter_name_changed)

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
    # MISC
    #

    def display_chapter_label(self):
        if not self.chapter_name:
            self.chapter_name = ""

        if self.location_items[self.location_index].callback:
            self.location_items[self.location_index].callback(self.chapter_name)
        else:
            self.action_base.set_top_label(self.chapter_name)