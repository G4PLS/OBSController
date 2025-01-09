from data.plugins.com_gapls_OBSController.actions.OBSAction import OBSAction
from src.backend.PluginManager.ActionBase import ActionBase
#from src.backend.Logging.Loggers.PluginLogger import plugin_logger
from GtkHelper.GtkHelper import better_disconnect

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw


class SwitchScene(OBSAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Action Events

    def on_ready(self):
        pass

    def on_update(self):
        pass

    # Ui Definition

    def build_ui(self):
        pass

    # Setting Loaders

    def load_settings(self):
        pass

    def load_ui_settings(self):
        pass

    # Ui Events

    def connect_events(self):
        pass

    def disconnect_events(self):
        pass

    # Displaying

    # Asset Management

    # Misc
