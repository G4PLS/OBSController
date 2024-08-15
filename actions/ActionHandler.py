import gi
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.PluginManager.PluginBase import PluginBase

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw


class ActionHandler(Adw.PreferencesGroup):
    def __init__(self, plugin_base: PluginBase, action_base: ActionBase, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_base: PluginBase = plugin_base
        self.action_base: ActionBase = action_base

        self.build_ui()

    def on_ready(self) -> None:
        pass

    def on_update(self) -> None:
        pass

    def on_click(self) -> None:
        pass

    def on_tick(self) -> None:
        pass

    def build_ui(self) -> None:
        pass

    def load_settings(self):
        pass

    def load_ui_settings(self):
        pass

    def show_error(self):
        pass