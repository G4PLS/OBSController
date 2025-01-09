import shlex

import gi

from GtkHelper.GtkHelper import better_disconnect
from ...globals import Icons, Colors
from ...internal.helper import run_command_detached

# from src.backend.Logging.Loggers.PluginLogger import plugin_logger

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

from ..OBSAction import OBSAction

class OpenOBS(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon_keys = [Icons.OBS]
        self.color_keys = [Colors.SECONDARY]

        self._icon_name = Icons.OBS
        self._color_name = Colors.SECONDARY

        self._current_icon = self.get_icon(self._icon_name)
        self._current_color = self.get_color(self._color_name)

        self.is_flatpak = False
        self.custom_command = None

    # Action Events

    def on_ready(self):
        self.load_settings()

    def on_update(self):
        self.show_icon()
        self.show_color()

    def on_short_up(self):
        command = ["obs"]

        if self.custom_command:
            command = shlex.split(self.custom_command)
        elif self.is_flatpak:
            command = ["flatpak", "run", "com.obsproject.Studio"]

        run_command_detached(command)

    # Ui Definition

    def build_ui(self):
        self.ui = Adw.PreferencesGroup()

        self.flatpak_switch = Adw.SwitchRow(title="Is Flatpak Installation")
        self.custom_command_entry = Adw.EntryRow(title="Custom Startup Command")

        self.ui.add(self.flatpak_switch)
        self.ui.add(self.custom_command_entry)

    # Setting Loaders

    def load_settings(self):
        settings = self.get_settings()

        self.is_flatpak = settings.get("is-flatpak", False)
        self.custom_command = settings.get("custom-command", None)

    def load_ui_settings(self):
        self.flatpak_switch.set_active(self.is_flatpak)
        self.custom_command_entry.set_text(self.custom_command or "")

    # Ui Events

    def connect_events(self):
        self.flatpak_switch.connect("notify::active", self.flatpak_switch_changed)
        self.custom_command_entry.connect("changed", self.custom_command_changed)

    def disconnect_events(self):
        better_disconnect(self.flatpak_switch, self.flatpak_switch_changed)
        better_disconnect(self.custom_command_entry, self.custom_command_changed)

    def flatpak_switch_changed(self, *args):
        settings = self.get_settings()

        self.is_flatpak = self.flatpak_switch.get_active()
        settings["is-flatpak"] = self.is_flatpak
        self.set_settings(settings)

    def custom_command_changed(self, *args):
        settings = self.get_settings()

        text = self.custom_command_entry.get_text()
        if text == "":
            self.custom_command = None
        else:
            self.custom_command = text

        settings["custom-command"] = self.custom_command
        self.set_settings(settings)

    # Displaying

    # Asset Managing

    # Misc