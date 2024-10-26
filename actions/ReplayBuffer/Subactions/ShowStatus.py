from ....internal.MultiAction.MultiActionItem import MultiActionItem
from ....internal.ComboAction.ComboActionRow import ComboActionRow, ComboActionItem
from ....internal.DuoPreferencesRow import DuoPreferencesRow

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class ShowStatus(MultiActionItem):
    FIELD_NAME = "Show Status"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_replay_buffer_state_changed",
                                                  self.buffer_state_changed)

    def on_tick(self):
        status = self.plugin_base.backend.get_replay_buffer_status()
        self.display_icon(status)

    #
    # MISC
    #

    def display_icon(self, status):
        if not status:
            return

        if status.get("output_active", True):
            self.action_base.set_background_color(self.plugin_base.asset_manager.PRIMARY_BACKGROUND)
            self.action_base.set_media(image=self.plugin_base.asset_manager.BUFFER_ON_MEDIA)
        else:
            self.action_base.set_background_color(self.plugin_base.asset_manager.SECONDARY_BACKGROUND)
            self.action_base.set_media(image=self.plugin_base.asset_manager.BUFFER_OFF_MEDIA)

    async def buffer_state_changed(self, *args):
        self.display_icon(args[2])