import gi

from ..MultiAction import MultiAction

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from .Subactions.StartStream import StartStream
from .Subactions.StopStream import StopStream
from .Subactions.ToggleStream import ToggleStream

class StreamAction(MultiAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_translation = {
            "start_stream": ("Start Streaming", StartStream),
            "stop_stream": ("Stop Streaming", StopStream),
            "toggle_stream": ("Toggle Stream", ToggleStream),
            "send_caption": ("Send Stream Caption", None),
        }

        self.action_lookup: str = "start_stream"

    def get_custom_config_area(self):
        self.ui = super().get_custom_config_area()

        self.load_ui_settings()

        self.connect_events()

        return self.ui