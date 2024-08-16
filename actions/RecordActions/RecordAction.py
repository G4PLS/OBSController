
import gi

from .Pause.PauseRecord import PauseRecord
from .Pause.ResumeRecord import ResumeRecord
from .Pause.TogglePause import TogglePause
from .Record.StartRecording import StartRecording
from .Record.StopRecording import StopRecording
from .Record.ToggleRecord import ToggleRecord
from ..MultiAction import MultiAction

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")


class RecordAction(MultiAction):
    """
    Actual action that will be used for StreamDeck, containing all SubActions
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_translation = {
            "start_record": ("Start Recording", StartRecording),
            "stop_record": ("Stop Recording", StopRecording),
            "pause_record": ("Pause Recording", PauseRecord),
            "resume_record": ("Resume Recording", ResumeRecord),
            "toggle_record": ("Toggle Recording", ToggleRecord),
            "toggle_pause": ("Toggle Pause", TogglePause)
        }

        self.action_lookup: str = "start_record"

    def get_custom_config_area(self):
        self.ui = super().get_custom_config_area()

        self.load_ui_settings()

        # CONNECT ALL EVENTS
        self.connect_events()

        return self.ui