from ....internal.MultiAction.MultiActionItem import MultiActionItem
from ....internal.ComboAction.ComboActionRow import ComboActionRow, ComboActionItem
from ....internal.DuoPreferencesRow import DuoPreferencesRow

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class StatusDisplay(MultiActionItem):
    FIELD_NAME = "Status Display"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_base.connect_to_backend_event("com.gapls.OBSController::OBSEvent", "on_virtualcam_state_changed",
                                                  self.cam_state_changed)

    #
    # ACTION EVENTS
    #

    def on_tick(self):
        status = self.plugin_base.backend.get_virtual_cam_status()

        if not status:
            self.action_base.set_background_color(self.plugin_base.asset_manager.SECONDARY_BACKGROUND)
            return

        self.display_icon(status)

    #
    # MISC
    #

    def display_icon(self, status):
        if status.get("output_active", True):
            self.action_base.set_background_color(self.plugin_base.asset_manager.PRIMARY_BACKGROUND)
            self.action_base.set_media(image=self.plugin_base.asset_manager.CAM_ON_MEDIA)
        else:
            self.action_base.set_background_color(self.plugin_base.asset_manager.SECONDARY_BACKGROUND)
            self.action_base.set_media(image=self.plugin_base.asset_manager.CAM_OFF_MEDIA)

    async def cam_state_changed(self, *args):
        self.display_icon(args[2])