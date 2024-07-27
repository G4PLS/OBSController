from typing import Tuple, Callable, Dict

from GtkHelper.GtkHelper import ComboRow

import gi

from ..OBSAction import OBSAction

from .Start_Record import StartRecord
from .Stop_Record import StopRecord

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class RecordAction(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_translation: Dict[str, Tuple[str, Callable]] = {
            "start_record": ("Start Recording", StartRecord.execute),
            "stop_record": ("Stop Recording", StopRecord.execute)
        }

        self.action_lookup: str = "start_record"

    def on_ready(self):
        self.load_settings()

    def get_config_rows(self) -> "list[Adw.PreferencesRow]":
        base_config = super().get_config_rows()
        self.action_model = Gtk.ListStore.new([str, str])

        self.action_row = ComboRow(title="Action", model=self.action_model)

        self.action_renderer = Gtk.CellRendererText()
        self.action_row.combo_box.pack_start(self.action_renderer, True)
        self.action_row.combo_box.add_attribute(self.action_renderer, "text", 0)

        self.load_action_model()
        self.load_ui_settings()

        self.connect_events()

        return base_config + [self.action_row]

    #
    # LOAD
    #

    def load_action_model(self):
        self.action_model.clear()

        for key, (display, _) in self.action_translation.items():
            if key:
                self.action_model.append([display, key])

    #
    # EVENTS
    #

    def connect_events(self):
        self.action_row.combo_box.connect("changed", self.on_action_changed)

    def disconnect_events(self):
        self.action_row.combo_box.disconnect_by_func(self.on_action_changed)

    #
    # SETTINGS
    #

    def load_ui_settings(self):
        for i, action_lookup in enumerate(self.action_model):
            if action_lookup[1] == self.action_lookup:
                self.action_row.combo_box.set_active(i)
                break
        else:
            self.action_row.combo_box.set_active(-1)

    def load_settings(self):
        settings = self.get_settings()

        self.action_lookup = settings.get("action-lookup", self.action_lookup)

    def on_action_changed(self, *args):
        settings = self.get_settings()

        self.action_lookup = self.action_model[self.action_row.combo_box.get_active()][1]

        settings["action-lookup"] = self.action_lookup
        self.set_settings(settings)

    #
    # ACTION
    #

    def on_key_down(self):
        self.action_translation.get(self.action_lookup)[1](self.plugin_base, self)