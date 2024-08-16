import gi

from src.backend.PluginManager.ActionBase import ActionBase

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")


class StreamActionHandler(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
