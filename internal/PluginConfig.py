from abc import abstractmethod, ABC

from src.backend.PluginManager.PluginBase import PluginBase

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import (Gtk, Adw)


class PluginConfigWindow(Adw.Window):
    def __init__(self, plugin_base: PluginBase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_base: PluginBase = plugin_base

        self.set_default_size(600, 300)

        self.conf_page = Adw.PreferencesPage()
        self.conf_settings = Adw.PreferencesGroup(title=f"{self.plugin_base.plugin_name} Config")
        self.conf_page.add(self.conf_settings)

        self.set_content(self.conf_page)

        self.connect("notify::is-active", self.on_active_notify)

        self.build()

    def on_active_notify(self, *args):
        if self.get_property("is-active"):
            self.present()
        else:
            self.close()

    @abstractmethod
    def build(self):
        pass

    def load_settings(self):
        pass

    def append(self, widget):
        self.conf_settings.add(widget)


class PluginConfigButton(Adw.PreferencesRow):
    def __init__(self, plugin_base: PluginBase, config_window: type[PluginConfigWindow], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_base: PluginBase = plugin_base
        self.config_window = config_window

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True)
        self.set_child(self.main_box)

        self.config_button = Gtk.Button(label="Open Config", hexpand=True, margin_start=12, margin_end=12, margin_top=5, margin_bottom=5)
        self.config_button.connect("clicked", self.open_config_window)

        self.main_box.append(self.config_button)

    def open_config_window(self, *args):
        config = self.config_window(self.plugin_base)
        config.present()
