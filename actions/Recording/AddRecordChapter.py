from src.backend.DeckManagement.InputIdentifier import InputEvent, Input
from src.backend.PluginManager.ActionBase import ActionBase
#from src.backend.Logging.Loggers.PluginLogger import plugin_logger
from GtkHelper.GtkHelper import better_disconnect
from ...globals import Icons, Colors
import gi

from GtkHelper.SearchComboRow import SearchComboRow

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ..OBSAction import OBSAction

from loguru import logger as log

import rpyc
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

class AddRecordChapter(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chapter_name: str = ""
        self.chapter_location: str = "top"

        self.icon_keys = [Icons.REC_CHAPTER]
        self.color_keys = [Colors.SECONDARY]

        self._icon_name = Icons.REC_CHAPTER
        self._color_name = Colors.SECONDARY

        self._current_icon = self.get_icon(self._icon_name)
        self._current_color = self.get_color(self._color_name)

    # Action Events

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        self.change_icon({})
        self.change_color({})

        self.show_icon()
        self.show_label()
        self.show_color()

    def on_short_up(self):
        if not self.chapter_name:
            return

        status_code = self.plugin_base.backend.custom_request("CreateRecordChapter", {"chapterName": self.chapter_name})

        if status_code == "501" or status_code == "702":
            log.warning(f"ADD RECORD CHAPTER RETUNRED: {status_code}")

    # Ui Definition

    def build_ui(self):
        self.ui = Adw.PreferencesGroup()

        self.chapter_name_entry = Adw.EntryRow(title="Record Chapter Name")
        self.chapter_locator = SearchComboRow(title="Chapter Name Location", use_single_line=True)

        self.ui.add(self.chapter_name_entry)
        self.ui.add(self.chapter_locator)
        self.ui.add(Gtk.Label(label="Only in Websocket version >=5.5.0 and only with Hybrid MP4"))

    # Setting Loaders
    def load_settings(self):
        settings = self.get_settings()

        self.chapter_name = settings.get("chapter-name", "")
        self.chapter_location = settings.get("chapter-location", "top")
        self._current_labels[self.chapter_location] = self.chapter_name

    def load_ui_settings(self):
        self.chapter_name_entry.set_text(self.chapter_name)

        positions = self.label_provider.generate_search_items()
        index = self.label_provider.get_index(self.chapter_location)

        self.chapter_locator.populate(positions, index)
        self.show_label()

    # Ui Events

    def connect_events(self):
        self.chapter_locator.connect("item-changed", self.chapter_location_changed)
        self.chapter_name_entry.connect("changed", self.chapter_name_changed)

    def disconnect_events(self):
        better_disconnect(self.chapter_locator, self.chapter_location_changed)
        better_disconnect(self.chapter_name_entry, self.chapter_name_changed)

    def chapter_name_changed(self, *args):
        settings = self.get_settings()

        self.chapter_name = self.chapter_name_entry.get_text()

        settings["chapter-name"] = self.chapter_name
        self.set_settings(settings)
        self._current_labels[self.chapter_location] = self.chapter_name

        self.show_label()

    def chapter_location_changed(self, _, item, *args):
        settings = self.get_settings()
        location = item.display_label

        self._current_labels[self.chapter_location] = ""
        self._current_labels[location] = self.chapter_name

        self.chapter_location = location
        settings["chapter-location"] = self.chapter_location
        self.set_settings(settings)

        self.show_label()

    # Displaying

    # Asset Managing

    # Misc
