from typing import Dict

import gi

from GtkHelper.GtkHelper import ComboRow
from src.backend.DeckManagement.InputIdentifier import InputEvent
from src.backend.PluginManager.ActionBase import ActionBase
from .MultiActionItem import MultiActionItem

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from loguru import logger as log


class MultiAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_lookup: Dict[str, type(MultiActionItem)] = {}
        self.action_translation: str = ""
        self.executing_action: MultiActionItem = None

    #
    # UI
    #

    def get_custom_config_area(self):
        """
        Not meant to be modified, use build_ui to define the UI of this Class
        """
        self.build_ui()  # Creates the MultiAction UI
        self.load_ui_settings()  # Loads the settings of the MultiAction UI
        self.load_item_ui()  # Loads the UI from the selected action
        self.connect_events()  # Connects the UI Events

        return self.ui

    def build_ui(self, ui: Adw.PreferencesGroup = None) -> Adw.PreferencesGroup:
        """
        Will either use a from-scratch ui or use the passed in ui
        @param ui: Pre-Defined UI, config selection will be added at the end of that UI
        @return: Returns the completed UI element
        """
        self.ui = ui or Adw.PreferencesGroup()

        self.action_model = Gtk.ListStore.new([str, str])

        self.action_row = ComboRow(title="Action", model=self.action_model)
        self.ui.add(self.action_row)

        self.action_renderer = Gtk.CellRendererText()
        self.action_row.combo_box.pack_start(self.action_renderer, True)
        self.action_row.combo_box.add_attribute(self.action_renderer, "text", 0)

        return self.ui

    #
    # UI EVENTS
    #

    def on_action_changed(self, *args):
        settings = self.get_settings()

        if self.executing_action:
            self.ui.remove(self.executing_action)

        self.action_translation = self.action_model[self.action_row.combo_box.get_active()][1]
        self.create_action_object(self.action_lookup.get(self.action_translation, None))
        self.load_item_ui()

        settings["action-lookup"] = self.action_translation
        self.set_settings(settings)

    def connect_events(self):
        self.action_row.combo_box.connect("changed", self.on_action_changed)

    def disconnect_events(self):
        try:
            self.action_row.combo_box.disconnect_by_func(self.on_action_changed)
        except:
            pass

    #
    # EVENTS
    #

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        if self.executing_action:
            self.executing_action.on_update()

    def on_tick(self):
        if self.executing_action:
            self.executing_action.on_tick()

    def event_callback(self, event: InputEvent, data: dict = None):
        if self.executing_action:
            self.executing_action.event_callback(event, data)

    #
    # SETTINGS
    #

    def load_settings(self):
        settings = self.get_settings()

        self.action_translation = settings.get("action-lookup", self.action_translation)
        self.create_action_object(self.action_lookup.get(self.action_translation, None))

    def load_ui_settings(self):
        self.load_action_model()

        for i, action_lookup in enumerate(self.action_model):
            if action_lookup[1] == self.action_translation:
                self.action_row.combo_box.set_active(i)
                break
        else:
            self.action_row.combo_box.set_active(-1)

    def load_action_model(self):
        self.action_model.clear()

        for key, item in self.action_lookup.items():
            self.action_model.append([item.FIELD_NAME, key])

    #
    # MISC
    #

    def create_action_object(self, action: type(MultiActionItem)):
        try:
            if not action:
                return
            self.executing_action = action(self.plugin_base, self)
            self.executing_action.build_ui()
            self.executing_action.on_ready()
        except:
            log.warning(
                f"Failed to load Action ({self.action_translation}) in MultiAction at {self.get_own_action_index()}")
            self.executing_action = None

    def load_item_ui(self):
        if self.executing_action:
            self.executing_action.unparent()
            self.ui.add(self.executing_action)
            self.executing_action.load_ui_settings()
            self.executing_action.connect_events()