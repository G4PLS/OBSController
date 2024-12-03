import subprocess

from ...OBSMultiActionItem import OBSMultiActionItem
from ....globals import Icons
from ....internal.MultiAction.MultiActionItem import MultiActionItem

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

# TODO: Add Icons
class OpenLastSave(OBSMultiActionItem):
    FIELD_NAME = "Open last Replay"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #
    # ACTION EVENTS
    #

    def on_update(self):
        self.action_base.set_background_color(self.secondary_color)

        _, render = self.plugin_base.asset_manager.icons.get_asset_values(Icons.OPEN_BUFFER)
        self.action_base.set_media(image=render)

    def on_key_down(self):
        status = self.plugin_base.backend.get_last_replay_buffer_replay()

        if not status:
            return

        replay_path = status.get("saved_replay_path", None)

        if replay_path:
            subprocess.Popen(f"xdg-open \"{replay_path}\"", shell=True, start_new_session=False)

    # Asyncs

    async def icon_changed(self, event: str, key: str, asset):
        if key in [Icons.SAVE_BUFFER]:
            self.on_update()

    def color_changed(self):
        self.on_update()