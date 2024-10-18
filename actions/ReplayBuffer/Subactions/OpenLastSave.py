import os
import subprocess
import threading
from copy import deepcopy

from src.backend.DeckManagement.Media.ImageLayer import ImageLayer
from src.backend.DeckManagement.Media.Media import Media
from ....internal.MultiAction.MultiActionItem import MultiActionItem
from ....internal.ComboAction.ComboActionRow import ComboActionRow, ComboActionItem
from ....internal.DuoPreferencesRow import DuoPreferencesRow

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

# TODO: Add Icons
class OpenLastSave(MultiActionItem):
    FIELD_NAME = "Open last Replay"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #
    # ACTION EVENTS
    #

    def on_key_down(self):
        status = self.plugin_base.backend.get_last_replay_buffer_replay()

        if not status:
            return

        replay_path = status.get("saved_replay_path", None)

        if replay_path:
            subprocess.Popen(f"xdg-open \"{replay_path}\"", shell=True, start_new_session=False)