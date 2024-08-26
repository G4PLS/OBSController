from typing import Dict, Tuple, Type

import gi

from GtkHelper.GtkHelper import ComboRow

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk

from .ActionHandler import ActionHandler
from .OBSAction import OBSAction

class MultiAction(OBSAction):
    """
    Specialized from of the OBSAction, makes it easier to create sub-action menus and define them
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_translation: Dict[str, Tuple[str, Type[ActionHandler]]] = {}

        self.action_lookup: str = ""
        self.selected_action: Tuple[str, Type[ActionHandler]] = None

    def on_ready(self):
        self.load_settings()

        if self.selected_action:
            self.selected_action.on_ready()

    def on_update(self):
        if self.selected_action:
            self.selected_action.on_update()

    def get_custom_config_area(self):
        self.ui = super().get_custom_config_area()

        self.action_model = Gtk.ListStore.new([str, str])

        self.action_row = ComboRow(title="Action", model=self.action_model)
        self.ui.add(self.action_row)

        self.action_renderer = Gtk.CellRendererText()
        self.action_row.combo_box.pack_start(self.action_renderer, True)
        self.action_row.combo_box.add_attribute(self.action_renderer, "text", 0)

        # LOAD CUSTOM UI
        #self.selected_action: Gtk.Widget

        self.selected_action.unparent()
        self.ui.add(self.selected_action)

        # SETUP UI SETTINGS
        self.load_action_model()

        return self.ui

    def load_action_model(self):
        self.action_model.clear()

        for key, (display, _) in self.action_translation.items():
            if key:
                self.action_model.append([display, key])

    def connect_events(self):
        self.action_row.combo_box.connect("changed", self.on_action_changed)

    def disconnect_events(self):
        try:
            self.action_row.combo_box.disconnect_by_func(self.on_action_changed)
        except:
            pass

    def load_ui_settings(self):
        for i, action_lookup in enumerate(self.action_model):
            if action_lookup[1] == self.action_lookup:
                self.action_row.combo_box.set_active(i)
                break
        else:
            self.action_row.combo_box.set_active(-1)

        self.selected_action.load_ui_settings()

    def load_settings(self):
        settings = self.get_settings()

        self.action_lookup = settings.get("action-lookup", self.action_lookup)

        self.selected_action = self.action_translation.get(self.action_lookup, None)

        if self.selected_action:
            self.selected_action = self.selected_action[1](self.plugin_base, self)
            self.selected_action.load_settings()

    def on_action_changed(self, *args):
        settings = self.get_settings()

        self.ui.remove(self.selected_action)

        self.action_lookup = self.action_model[self.action_row.combo_box.get_active()][1]

        self.selected_action = self.action_translation.get(self.action_lookup, None)

        if self.selected_action and len(self.selected_action) >= 1:

            self.selected_action = self.selected_action[1](self.plugin_base, self)

            self.ui.add(self.selected_action)

            self.selected_action.on_ready()
            self.selected_action.load_settings()
            self.selected_action.load_ui_settings()

        settings["action-lookup"] = self.action_lookup
        self.set_settings(settings)

    def on_key_down(self):
        if self.selected_action:
            self.selected_action.on_click()

    def on_tick(self):
        if self.selected_action:
            self.selected_action.on_tick()