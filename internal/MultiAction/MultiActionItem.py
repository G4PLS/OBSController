import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

from src.backend.DeckManagement.InputIdentifier import InputEvent, Input
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionBase import ActionBase

class MultiActionItem(Adw.PreferencesGroup):
    FIELD_NAME: str = "Action"

    def __init__(self, plugin_base: PluginBase, action_base: ActionBase, *args, **kwargs):
        super().__init__(title=self.FIELD_NAME, *args, **kwargs)

        self.plugin_base = plugin_base
        self.action_base = action_base

    #
    # UI
    #

    def build_ui(self):
        pass

    #
    # UI EVENTS
    #

    def connect_events(self):
        pass

    def disconnect_events(self):
        pass

    #
    # ACTION EVENTS
    #

    def on_ready(self):
        pass

    def on_update(self):
        pass

    def on_tick(self):
        pass

    def event_callback(self, event: InputEvent, data: dict = None):
        if event in (Input.Key.Events.DOWN,
                     Input.Dial.Events.DOWN,
                     Input.Dial.Events.SHORT_TOUCH_PRESS):
            self.on_key_down()
        elif event in (Input.Key.Events.UP,
                       Input.Dial.Events.UP):
            self.on_key_up()

    def on_key_down(self):
        pass

    def on_key_up(self):
        pass

    #
    # SETTINGS
    #

    def load_settings(self):
        pass

    def load_ui_settings(self):
        pass

    def get_settings(self):
        return self.action_base.get_settings()

    def set_settings(self, settings):
        self.action_base.set_settings(settings)

    #
    # MISC
    #

    def get_asset_path(self, asset_name: str, subdirs: list[str] = [], asset_folder: str = "assets"):
        return self.action_base.get_asset_path(asset_name, subdirs, asset_folder)